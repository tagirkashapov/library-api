from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import status

from app.core import EntityNotFound, NoFieldsToUpdate
from app.schemas import AuthorResponse
from app.services import AuthorService
from app.api import get_author_service
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
def mock_authors():
    return [
        AuthorResponse(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name="Author One"
        ),
        AuthorResponse(
            id=2,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name="Author Two"
        ),
        AuthorResponse(
            id=3,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name="Author Three"
        )
    ]


@pytest.fixture
def create_data():
    return [
        {"name": "Author One"},
        {"name": "Author Two"}
    ]


@pytest.fixture
def update_data():
    return {"name": "Author Three"}


@pytest.fixture
async def mock_client(mock_service):
    app.dependency_overrides[get_author_service] = lambda: mock_service
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as async_client:
        yield async_client
    app.dependency_overrides.clear()


async def test_create_author_succes(
    mock_service: AuthorService,
    mock_authors: list[AuthorResponse],
    mock_client: AsyncClient,
    create_data
):
    mock_service.create.return_value = mock_authors[0]

    response = await mock_client.post("/authors", json=create_data[0])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == mock_authors[0].model_dump(mode="json")


async def test_get_author_succes(
    mock_service: AuthorService,
    mock_authors: list[AuthorResponse],
    mock_client: AsyncClient,
):
    mock_service.get_by_id.return_value = mock_authors[0]

    response = await mock_client.get(f"/authors/{1}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_authors[0].model_dump(mode="json")


async def test_get_author_not_found(
    mock_service: AuthorService,
    mock_client: AsyncClient,
):
    mock_service.get_by_id.side_effect = EntityNotFound("Author", 1)

    response = await mock_client.get(f"/authors/{1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Author" in response.json()["detail"]


async def test_get_authors_with_data(
    mock_service: AuthorService,
    mock_authors: list[AuthorResponse],
    mock_client: AsyncClient,
):
    mock_service.get_all.return_value = mock_authors[:2]

    response = await mock_client.get("/authors")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        author.model_dump(mode="json") for author in mock_authors[:2]
    ]


async def test_get_authors_empty(
    mock_service: AuthorService,
    mock_client: AsyncClient,
):
    mock_service.get_all.return_value = []

    response = await mock_client.get("/authors")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


async def test_update_author(
    mock_service: AuthorService,
    mock_authors: list[AuthorResponse],
    mock_client: AsyncClient,
    update_data
):
    mock_service.update.return_value = mock_authors[2]

    response = await mock_client.patch(f"/authors/{1}", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_authors[2].model_dump(mode="json")


async def test_update_author_not_found(
    mock_service: AuthorService,
    mock_client: AsyncClient,
    update_data
):
    mock_service.update.side_effect = EntityNotFound("Author", 999)

    response = await mock_client.patch(f"/authors/{1}", json=update_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Author" in response.json()["detail"]


async def test_update_author_no_fields(
    mock_service: AuthorService,
    mock_client: AsyncClient,
):
    mock_service.update.side_effect = NoFieldsToUpdate("Author")

    response = await mock_client.patch(f"/authors/{1}", json={})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Author" in response.json()["detail"]


async def test_delete_author(
    mock_service: AuthorService,
    mock_client: AsyncClient,
):
    mock_service.delete.return_value = None

    response = await mock_client.delete(f"/authors/{1}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_author_not_found(
    mock_service: AuthorService,
    mock_authors: list[AuthorResponse],
    mock_client: AsyncClient,
):
    mock_service.delete.side_effect = EntityNotFound("Author", 999)

    response = await mock_client.delete(f"/authors/{1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Author" in response.json()["detail"]
