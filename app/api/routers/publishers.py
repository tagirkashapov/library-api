from fastapi import APIRouter, Depends, HTTPException, status

from app.core.exceptions import EntityNotFound
from app.schemas import PublisherResponse, PublisherCreate, PublisherUpdate
from app.services import PublisherService
from app.api.dependencies import get_publisher_service

router = APIRouter(prefix="/publishers")


@router.get("", response_model=list[PublisherResponse], tags=["Publishers"])
def get_publishers(
    publisher_service: PublisherService = Depends(get_publisher_service)
) -> list[PublisherResponse]:
    """Получить список всех издательств"""
    return publisher_service.get_publishers()


@router.get(
    "/{publisher_id}", response_model=PublisherResponse, tags=["Publishers"]
)
def get_publisher(
    publisher_id: int,
    publisher_service: PublisherService = Depends(get_publisher_service)
) -> list[PublisherResponse]:
    """Получить издательство по id"""
    try:
        return publisher_service.get_publisher(publisher_id)
    except EntityNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found"
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PublisherResponse,
    tags=["Publishers"]
)
def create_publisher(
    publisher_create: PublisherCreate,
    publisher_service: PublisherService = Depends(get_publisher_service)
) -> PublisherResponse:
    """Создать издательство"""
    return publisher_service.create_publisher(publisher_create)


@router.patch(
    "/{publisher_id}", response_model=PublisherResponse, tags=["Publishers"]
)
def update_publisher(
    publisher_id: int,
    publisher_update: PublisherUpdate,
    publisher_service: PublisherService = Depends(get_publisher_service)
) -> PublisherResponse:
    """Обновить данные издательства по id"""
    try:
        return publisher_service.update_publisher(
            publisher_id, publisher_update
        )
    except EntityNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found"
        )


@router.delete(
    "/{publisher_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Publishers"]
)
def get_publishers(
    publisher_id: int,
    publisher_service: PublisherService = Depends(get_publisher_service)
) -> None:
    """Удалить издательство по id"""
    try:
        publisher_service.delete_publisher(publisher_id)
    except EntityNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Publisher not found"
        )
