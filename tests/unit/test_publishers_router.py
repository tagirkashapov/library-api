from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import status

from app.core import EntityNotFound, NoFieldsToUpdate
from app.schemas import PublisherResponse
from app.services import PublisherService
from app.api import get_publisher_service
from app.main import app


@pytest.fixture
def mock_service():
    service = MagicMock()
    service.get_all = AsyncMock()
    service.get_by_id = AsyncMock()
    service.create = AsyncMock()
    service.update = AsyncMock()
    service.delete = AsyncMock()
    return service


@pytest.fixture
def mock_publishers():
    return [
        PublisherResponse(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name="Publisher One"
        ),
        PublisherResponse(
            id=2,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name="Publisher Two"
        ),
        PublisherResponse(
            id=3,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name="Publisher Three"
        )
    ]


@pytest.fixture
def create_data():
    return [
        {"name": "Publisher One"},
        {"name": "Publisher Two"}
    ]


@pytest.fixture
def update_data():
    return {"name": "Publisher Three"}


@pytest.fixture
async def mock_client(mock_service):
    app.dependency_overrides[get_publisher_service] = lambda: mock_service
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as async_client:
        yield async_client
    app.dependency_overrides.clear()


async def test_create_publisher_succes(
    mock_service: PublisherService,
    mock_publishers: list[PublisherResponse],
    mock_client: AsyncClient,
    create_data
):
    mock_service.create.return_value = mock_publishers[0]

    response = await mock_client.post("/publishers", json=create_data[0])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == mock_publishers[0].model_dump(mode="json")


async def test_get_publisher_succes(
    mock_service: PublisherService,
    mock_publishers: list[PublisherResponse],
    mock_client: AsyncClient,
):
    mock_service.get_by_id.return_value = mock_publishers[0]

    response = await mock_client.get(f"/publishers/{1}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_publishers[0].model_dump(mode="json")


async def test_get_publisher_not_found(
    mock_service: PublisherService,
    mock_client: AsyncClient,
):
    mock_service.get_by_id.side_effect = EntityNotFound("Publisher", 1)

    response = await mock_client.get(f"/publishers/{1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Publisher" in response.json()["detail"]


async def test_get_publishers_with_data(
    mock_service: PublisherService,
    mock_publishers: list[PublisherResponse],
    mock_client: AsyncClient,
):
    mock_service.get_all.return_value = mock_publishers[:2]

    response = await mock_client.get("/publishers")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        publisher.model_dump(mode="json") for publisher in mock_publishers[:2]
    ]


async def test_get_publishers_empty(
    mock_service: PublisherService,
    mock_client: AsyncClient,
):
    mock_service.get_all.return_value = []

    response = await mock_client.get("/publishers")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


async def test_update_publisher(
    mock_service: PublisherService,
    mock_publishers: list[PublisherResponse],
    mock_client: AsyncClient,
    update_data
):
    mock_service.update.return_value = mock_publishers[2]

    response = await mock_client.patch(f"/publishers/{1}", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_publishers[2].model_dump(mode="json")


async def test_update_publisher_not_found(
    mock_service: PublisherService,
    mock_client: AsyncClient,
    update_data
):
    mock_service.update.side_effect = EntityNotFound("Publisher", 999)

    response = await mock_client.patch(f"/publishers/{1}", json=update_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Publisher" in response.json()["detail"]


async def test_update_publisher_no_fields(
    mock_service: PublisherService,
    mock_client: AsyncClient,
):
    mock_service.update.side_effect = NoFieldsToUpdate("Publisher")

    response = await mock_client.patch(f"/publishers/{1}", json={})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Publisher" in response.json()["detail"]


async def test_delete_publisher(
    mock_service: PublisherService,
    mock_client: AsyncClient,
):
    mock_service.delete.return_value = None

    response = await mock_client.delete(f"/publishers/{1}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_publisher_not_found(
    mock_service: PublisherService,
    mock_publishers: list[PublisherResponse],
    mock_client: AsyncClient,
):
    mock_service.delete.side_effect = EntityNotFound("Publisher", 999)

    response = await mock_client.delete(f"/publishers/{1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Publisher" in response.json()["detail"]
