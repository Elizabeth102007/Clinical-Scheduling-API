from sqlmodel import SQLModel, Field, Column, DateTime
from typing import Optional
from datetime import datetime, timezone


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    age: int
    diagnosis: str
    is_active: bool=True
    created_at: datetime = Field(default_factory=get_utc_now,
                                 sa_column=Column(DateTime(timezone=True), nullable=False))

class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    doctor_name: str
    appointment_time: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    reason: str
    status: str = Field(default="scheduled")
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )