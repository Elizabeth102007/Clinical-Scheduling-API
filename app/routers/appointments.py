from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.database import get_db
from app.models import Patient, Appointment
from app.schemas import AppointmentCreate, AppointmentRead, AppointmentUpdate

router = APIRouter()

AsyncSessionDep= Annotated[AsyncSession, Depends(get_db)]

@router.post("/", 
             response_model=AppointmentRead,
             status_code=status.HTTP_201_CREATED)
async def create_appointment(session:AsyncSessionDep, a_create: AppointmentCreate):
    patient = await session.get(Patient, a_create.patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Patient with the identity{a_create.patient_id} doesn't exist"
        )
    db_appointment = Appointment.model_validate(a_create)
    session.add(db_appointment)
    await session.commit()
    await session.refresh(db_appointment)
    return db_appointment

@router.get("/",
            response_model=list[AppointmentRead],
            status_code=status.HTTP_200_OK)
async def get_appointments(session: AsyncSessionDep,
                           patient_id: Optional[int] = Query(default=None, 
                                                             description="Filter appointments by patient ID"),
                           offset: int=0, 
                           limit: Annotated[int, Query(le=100)]=100):
    
    stmt = select(Appointment)
    if patient_id is not None:
        stmt = stmt.where(Appointment.patient_id==patient_id)
    stmt = stmt.offset(offset).limit(limit)
    result = await session.exec(stmt)
    appointments = result.all()
    return appointments

@router.get("/{appointment_id}",
            response_model=AppointmentRead,
            status_code=status.HTTP_200_OK)
async def get_a_appointment(session: AsyncSessionDep, appointment_id: int):
    appointment = await session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Appointment with ID {appointment_id} not found"
        )
    return appointment

@router.patch("/{appointment_id}",
              response_model= AppointmentRead,
              status_code=status.HTTP_200_OK)
async def update_appointment(session: AsyncSessionDep, 
                             a_update: AppointmentUpdate, 
                             appointment_id: int):
    db_appointment = await session.get(Appointment, appointment_id)
    if not db_appointment:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )
    update_data = a_update.model_dump(exclude_unset=True)
    
    db_appointment.sqlmodel_update(update_data)
    session.add(db_appointment)
    await session.commit()
    await session.refresh(db_appointment)
    return db_appointment

@router.delete("/{appointment_id}",status_code= status.HTTP_204_NO_CONTENT)
async def delete_apppointment(appointment_id:int, session: AsyncSessionDep):
    appointment = await session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )
    await session.delete(appointment)
    await session.commit()
    return None
    