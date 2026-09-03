from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlmodel import SQLModel

from app.config import settings
from app.database import engine
from app.routers import patients, appointments

api_key_header = APIKeyHeader(name= "X-Api-Key", auto_error=False)

def validate_api_key(x_api_key: str | None = Depends(api_key_header)):
    if not x_api_key or x_api_key != settings.API_KEY.get_secret_value():
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid API key"
        )

async def init_db():
    async with engine.begin() as conn:
          await conn.run_sync(SQLModel.metadata.create_all)
    

@asynccontextmanager
async def lifespan(app: FastAPI):
      await init_db()
      yield

app = FastAPI(lifespan=lifespan, 
              dependencies=[Depends(validate_api_key)], 
              title=settings.APP_NAME)


# mount the router with prefix and OpenAPI tags
app.include_router(
    patients.router,
    prefix="/patients",
    tags=["Patients"]
)

app.include_router(
     appointments.router,
     prefix="/appointments",
     tags=["Appointments"]
)