from fastapi import APIRouter, status, HTTPException, Depends

from app.core.exceptions import BookNotFound
from app.schemas.book import BookResponse, BookCreate, BookUpdate
from app.services.book import BookService
from app.api.dependencies import get_book_service

router = APIRouter(prefix="/books")


@router.get("", response_model=list[BookResponse], tags=["Books"])
def get_books(
    book_service: BookService = Depends(get_book_service)
) -> list[BookResponse]:
    """Получить список всех книг"""
    return book_service.get_books()


@router.get("/{book_id}", response_model=BookResponse, tags=["Books"])
def get_book(
    book_id: int,
    book_service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Получить книгу по id"""
    try:
        return book_service.get_book(book_id)
    except BookNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=BookResponse,
    tags=["Books"]
)
def create_book(
    book_create: BookCreate,
    book_service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Создать книгу"""
    return book_service.create_book(book_create)


@router.patch("/{book_id}", response_model=BookResponse, tags=["Books"])
def update_book(
    book_id: int,
    book_update: BookUpdate,
    book_service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Обновить данные книги по id"""
    try:
        return book_service.update_book(book_id, book_update)
    except BookNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"]
)
def delete_book(
    book_id: int,
    book_service: BookService = Depends(get_book_service)
) -> None:
    """Удалить книгу по id"""
    try:
        return book_service.delete_book(book_id)
    except BookNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
