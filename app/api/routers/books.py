from fastapi import APIRouter, Depends, status

from app.schemas import (
    BookResponse, BookDetailResponse, BookCreate, BookUpdate
)
from app.services import BookService
from app.api import get_book_service

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=list[BookResponse])
async def get_books(
    book_service: BookService = Depends(get_book_service)
) -> list[BookResponse]:
    return await book_service.get_all()


@router.get("/{book_id}", response_model=BookDetailResponse)
async def get_book(
    book_id: int,
    book_service: BookService = Depends(get_book_service)
) -> BookDetailResponse:
    return await book_service.get_by_id(book_id)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=BookResponse
)
async def create_book(
    create_data: BookCreate,
    book_service: BookService = Depends(get_book_service)
) -> BookResponse:
    return await book_service.create(create_data)


@router.patch("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    update_data: BookUpdate,
    book_service: BookService = Depends(get_book_service)
) -> BookResponse:
    return await book_service.update(book_id, update_data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    book_service: BookService = Depends(get_book_service) 
) -> None:
    await book_service.delete(book_id)
