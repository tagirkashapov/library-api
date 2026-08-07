from fastapi import APIRouter, Depends, HTTPException, status

from app.core.exceptions import EntityNotFound
from app.schemas import AuthorResponse, AuthorCreate, AuthorUpdate
from app.services import AuthorService
from app.api.dependencies import get_author_service

router = APIRouter(prefix="/authors")


@router.get("", response_model=list[AuthorResponse], tags=["Authors"])
def get_authors(
    author_service: AuthorService = Depends(get_author_service)
) -> list[AuthorResponse]:
    """Получить список всех авторов"""
    return author_service.get_authors()


@router.get("/{author_id}", response_model=AuthorResponse, tags=["Authors"])
def get_author(
    author_id: int, author_service: AuthorService = Depends(get_author_service)
) -> list[AuthorResponse]:
    """Получить автороа по id"""
    try:
        return author_service.get_author(author_id)
    except EntityNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthorResponse,
    tags=["Authors"]
)
def create_author(
    author_create: AuthorCreate,
    author_service: AuthorService = Depends(get_author_service)
) -> AuthorResponse:
    """Создать автора"""
    return author_service.create_author(author_create)


@router.patch("/{author_id}", response_model=AuthorResponse, tags=["Authors"])
def update_author(
    author_id: int,
    author_update: AuthorUpdate,
    author_service: AuthorService = Depends(get_author_service)
) -> AuthorResponse:
    """Обновить данные автора по id"""
    try:
        return author_service.update_author(author_id, author_update)
    except EntityNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )


@router.delete(
    "/{author_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Authors"]
)
def get_authors(
    author_id: int, author_service: AuthorService = Depends(get_author_service)
) -> None:
    """Удалить автора по id"""
    try:
        author_service.delete_author(author_id)
    except EntityNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
