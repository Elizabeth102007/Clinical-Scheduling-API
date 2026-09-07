
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from app.models import StatusEnum
class PatientBase(SQLModel):
    full_name: str = Field(min_length=2, max_length=130)
    age: int = Field(gt=0)
    diagnosis: str

class PatientCreate(PatientBase):
      pass

class PatientRead(PatientBase):
     id: int
     is_active: bool
     created_at: datetime

class PatientUpdate(SQLModel):
     full_name: Optional[str] = Field(default=None,min_length=2, max_length=130)
     age: Optional[int] = Field(default=None, gt=0)
     diagnosis: Optional[str]= None
     is_active: Optional[bool] = None

class AppointmentBase(SQLModel):
     patient_id: int 
     doctor_name: str = Field(min_length=2, max_length=140)
     appointment_time: datetime
     reason: str

class AppointmentCreate(AppointmentBase):
     status:  StatusEnum = StatusEnum.SCH

class AppointmentRead(AppointmentBase):
     id: int
     status: StatusEnum 
     created_at : datetime

class AppointmentUpdate(SQLModel):
     doctor_name: Optional[str] = Field(default=None, min_length=2, max_length=140)
     reason: Optional[str] = None
     appointment_time: Optional[datetime] = None
     status: Optional[StatusEnum] = None