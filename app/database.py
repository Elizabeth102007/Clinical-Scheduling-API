from sqlmodel.ext.asyncio.session import  AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import settings

engine = create_async_engine(str(settings.DATABASE_URL), 
                             pool_size=5, 
                             max_overflow=10)

AsyncSessionLocal = async_sessionmaker(bind=engine, 
                                      class_=AsyncSession, 
                                      expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

