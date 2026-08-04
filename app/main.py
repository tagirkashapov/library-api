from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.db import engine
from app.db.base import Base
from app.api.books import router as book_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(book_router)
