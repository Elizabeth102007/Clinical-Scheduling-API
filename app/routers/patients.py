from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.database import get_db
from app.models import Patient
from app.schemas import PatientCreate, PatientRead, PatientUpdate

router = APIRouter()

AsyncSessionDep= Annotated[AsyncSession, Depends(get_db)]

@router.post("/", 
             response_model=PatientRead, 
             status_code= status.HTTP_201_CREATED)

async def create_patient(session: AsyncSessionDep, patientcreate:PatientCreate):
    db_patient = Patient.model_validate(patientcreate)
    session.add(db_patient)
    await session.commit()
    await session.refresh(db_patient)
    return db_patient


@router.get("/",
             response_model=list[PatientRead],
             status_code= status.HTTP_200_OK)

async def get_patients(session: AsyncSessionDep, 
                       offset: int= 0, 
                       limit: Annotated[int, Query(le=100)]= 100):
    statement = select(Patient).offset(offset).limit(limit)
    result = await session.exec(statement)
    patients = result.all()
    return patients


@router.get("/{patient_id}",
            response_model=PatientRead,
            status_code=status.HTTP_200_OK)

async def get_a_patient(session: AsyncSessionDep, patient_id:int):
    patient = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Patient not found"
        )
    return patient

@router.patch("/{patient_id}", 
              response_model=PatientRead,
              status_code=status.HTTP_200_OK)
async def update_patient(session: AsyncSessionDep, 
                         patient_update:PatientUpdate, 
                         patient_id: int):
    db_patient = await session.get(Patient, patient_id)
    if not db_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    update_data = patient_update.model_dump(exclude_unset=True)

    db_patient.sqlmodel_update(update_data)
    session.add(db_patient)
    await session.commit()
    await session.refresh(db_patient)
    return db_patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int, session: AsyncSessionDep):
    patient = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    await session.delete(patient)
    await session.commit()
    return None
