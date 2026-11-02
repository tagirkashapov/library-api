from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db import get_db
from app.services import PublisherService, AuthorService

async def get_publisher_service(
    db: AsyncSession = Depends(get_db)
) -> PublisherService:
    return PublisherService(db)

async def get_author_service(
    db: AsyncSession = Depends(get_db)
) -> AuthorService:
    return AuthorService(db)
