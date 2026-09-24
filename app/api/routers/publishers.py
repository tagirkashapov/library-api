from fastapi import APIRouter, Depends, status

from app.schemas import PublisherResponse, PublisherCreate, PublisherUpdate
from app.services import PublisherService
from app.api import get_publisher_service

router = APIRouter(prefix="/publishers", tags=["Publishers"])


@router.get("", response_model=list[PublisherResponse])
async def get_publishers(
    publisher_service: PublisherService = Depends(get_publisher_service)
) -> list[PublisherResponse]:
    return await publisher_service.get_all()


@router.get("/{publisher_id}", response_model=PublisherResponse)
async def get_publisher(
    publisher_id: int,
    publisher_service: PublisherService = Depends(get_publisher_service)
) -> PublisherResponse:
    return await publisher_service.get_by_id(publisher_id)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=PublisherResponse
)
async def create_publisher(
    create_data: PublisherCreate,
    publisher_service: PublisherService = Depends(get_publisher_service)
) -> PublisherResponse:
    return await publisher_service.create(create_data)


@router.patch("/{publisher_id}", response_model=PublisherResponse)
async def update_publisher(
    publisher_id: int,
    update_data: PublisherUpdate,
    publisher_service: PublisherService = Depends(get_publisher_service)
) -> PublisherResponse:
    return await publisher_service.update(publisher_id, update_data)


@router.delete("/{publisher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_publisher(
    publisher_id: int,
    publisher_service: PublisherService = Depends(get_publisher_service) 
) -> None:
    await publisher_service.delete(publisher_id)
