from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, date

import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import status

from app.core import EntityNotFound, NoFieldsToUpdate
from app.schemas import (
    PublisherShortResponse,
    AuthorShortResponse,
    BookResponse,
    BookDetailResponse,
)
from app.services import BookService
from app.api import get_book_service
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
def mock_books():
    return [
        BookResponse(
            id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            title="Book One",
            publication_date=date(2001, 1, 1),
            isbn="9785948242736",
            publisher_id=1,
            author_ids=[1, 2]
        ),
        BookResponse(
            id=2,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            title="Book Two",
            publication_date=date(2002, 2, 2),
            isbn="9785041002237",
            publisher_id=2,
            author_ids=[1, 3]
        ),
        BookResponse(
            id=3,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            title="Book Three",
            publication_date=date(2003, 3, 3),
            isbn="9783161484100",
            publisher_id=3,
            author_ids=[2, 3]
        )
    ]


@pytest.fixture
def create_data():
    return [
        {
            "title": "Book One",
            "publication_date": "2001-01-01",
            "isbn": "9785948242736",
            "publisher_id": 1,
            "author_ids": [1, 2]
        },
        {
            "title": "Book Two",
            "publication_date": "2002-02-02",
            "isbn": "9785041002237",
            "publisher_id": 2,
            "author_ids": [1, 3]
        }
    ]


@pytest.fixture
def update_data():
    return {
        "title": "Book Three",
        "publication_date": "2003-03-03",
        "isbn": "9783161484100",
        "publisher_id": 3,
        "author_ids": [2, 3]
    }


@pytest.fixture
async def mock_client(mock_service):
    app.dependency_overrides[get_book_service] = lambda: mock_service
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as async_client:
        yield async_client
    app.dependency_overrides.clear()


async def test_create_book_succes(
    mock_service: BookService,
    mock_books: list[BookResponse],
    mock_client: AsyncClient,
    create_data
):
    mock_service.create.return_value = mock_books[0]

    response = await mock_client.post("/books", json=create_data[0])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == mock_books[0].model_dump(mode="json")


async def test_get_by_id_succes(
    mock_service: BookService,
    mock_client: AsyncClient
):
    mock_book = BookDetailResponse(
        id=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        title="Book One",
        publication_date=date(2001, 1, 1),
        isbn="9785948242736",
        publisher=PublisherShortResponse(id=1, name="Publisher One"),
        authors=[
            AuthorShortResponse(id=1, name="Author One"),
            AuthorShortResponse(id=2, name="Author Two")
        ]
    )
    mock_service.get_by_id.return_value = mock_book

    response = await mock_client.get(f"/books/{1}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_book.model_dump(mode="json")


async def test_get_by_id_not_found(
    mock_service: BookService,
    mock_client: AsyncClient
):
    mock_service.get_by_id.side_effect = EntityNotFound("Book", 1)

    response = await mock_client.get(f"/books/{1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Book" in response.json()["detail"]


async def test_get_books_with_data(
    mock_service: BookService,
    mock_books: list[BookResponse],
    mock_client: AsyncClient
):
    mock_service.get_all.return_value = mock_books[:2]

    response = await mock_client.get("/books")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        book.model_dump(mode="json") for book in mock_books[:2]
    ]


async def test_get_books_empty(
    mock_service: BookService,
    mock_client: AsyncClient
):
    mock_service.get_all.return_value = []

    response = await mock_client.get("/books")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


async def test_update_book(
    mock_service: BookService,
    mock_books: list[BookResponse],
    mock_client: AsyncClient,
    update_data
):
    mock_service.update.return_value = mock_books[2]

    response = await mock_client.patch(f"/books/{1}", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_books[2].model_dump(mode="json")


async def test_update_book_not_found(
    mock_service: BookService,
    mock_client: AsyncClient,
    update_data
):
    mock_service.update.side_effect = EntityNotFound("Book", 999)

    response = await mock_client.patch(f"/books/{1}", json=update_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Book" in response.json()["detail"]


async def test_update_book_no_fields(
    mock_service: BookService,
    mock_client: AsyncClient
):
    mock_service.update.side_effect = NoFieldsToUpdate("Book")

    response = await mock_client.patch(f"/books/{1}", json={})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Book" in response.json()["detail"]


async def test_delete_book(
    mock_service: BookService,
    mock_client: AsyncClient
):
    mock_service.delete.return_value = None

    response = await mock_client.delete(f"/books/{1}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_book_not_found(
    mock_service: BookService,
    mock_books: list[BookResponse],
    mock_client: AsyncClient
):
    mock_service.delete.side_effect = EntityNotFound("Book", 999)

    response = await mock_client.delete(f"/books/{1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Book" in response.json()["detail"]
