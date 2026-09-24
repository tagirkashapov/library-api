from fastapi import APIRouter, Depends, status

from app.schemas import AuthorResponse, AuthorCreate, AuthorUpdate
from app.services import AuthorService
from app.api import get_author_service

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("", response_model=list[AuthorResponse])
async def get_authors(
    author_service: AuthorService = Depends(get_author_service)
) -> list[AuthorResponse]:
    return await author_service.get_all()


@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
    author_id: int,
    author_service: AuthorService = Depends(get_author_service)
) -> AuthorResponse:
    return await author_service.get_by_id(author_id)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=AuthorResponse
)
async def create_Author(
    create_data: AuthorCreate,
    author_service: AuthorService = Depends(get_author_service)
) -> AuthorResponse:
    return await author_service.create(create_data)


@router.patch("/{author_id}", response_model=AuthorResponse)
async def update_Author(
    author_id: int,
    update_data: AuthorUpdate,
    author_service: AuthorService = Depends(get_author_service)
) -> AuthorResponse:
    return await author_service.update(author_id, update_data)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_Author(
    author_id: int,
    author_service: AuthorService = Depends(get_author_service) 
) -> None:
    await author_service.delete(author_id)
