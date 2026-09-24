import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core import get_settings
from app.db import Base

settings = get_settings()
settings.POSTGRES_DB = "library_test"


@pytest.fixture()
async def db():
    engine = create_async_engine(settings.DATABASE_URL)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
    
    async with SessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()
