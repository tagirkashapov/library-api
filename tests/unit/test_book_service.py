from unittest.mock import AsyncMock
from datetime import datetime, date

import pytest

from app.core import EntityNotFound, NoFieldsToUpdate
from app.schemas import (
    PublisherResponse,
    PublisherShortResponse,
    AuthorResponse,
    AuthorShortResponse,
    BookResponse,
    BookDetailResponse,
    BookCreate,
    BookUpdate
)
from app.services import BookService


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    return db


@pytest.fixture
def book_service(mock_db):
    service = BookService(mock_db)
    service.repository = AsyncMock()
    service.publisher_repository = AsyncMock()
    service.author_repository = AsyncMock()
    service.repository.model.__name__ = "Book"
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
        BookCreate(
            title="Book One",
            publication_date=date(2001, 1, 1),
            isbn="9785948242736",
            publisher_id=1,
            author_ids=[1, 2]
        ),
        BookCreate(
            title="Book Two",
            publication_date=date(2002, 2, 2),
            isbn="9785041002237",
            publisher_id=2,
            author_ids=[1, 3]
        )
    ]


@pytest.fixture
def update_data():
    return BookUpdate(
        title="Book Three",
        publication_date=date(2003, 3, 3),
        isbn="9783161484100",
        publisher_id=3,
        author_ids=[2, 3]
    )


async def test_create_success(
    book_service: BookService,
    mock_publishers: list[PublisherResponse],
    mock_authors: list[AuthorResponse],
    mock_books: list[BookResponse],
    create_data: list[BookCreate]
):
    book_service.publisher_repository.get_by_id.return_value = (
        mock_publishers[0]
    )
    book_service.author_repository.get_by_ids.return_value = mock_authors[:2]
    book_service.repository.create.return_value = mock_books[0]

    created = await book_service.create(create_data[0])

    assert created.id == mock_books[0].id
    assert created.created_at == mock_books[0].created_at
    assert created.updated_at == mock_books[0].updated_at
    assert created.title == mock_books[0].title


async def test_get_by_id_succes(book_service: BookService):
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
    book_service.repository.get_by_id.return_value = mock_book

    fetched = await book_service.get_by_id(1)

    assert fetched.id == mock_book.id
    assert fetched.title == mock_book.title
    assert fetched.publisher == mock_book.publisher
    assert fetched.authors == mock_book.authors


async def test_get_by_id_not_found(book_service: BookService):
    book_service.repository.get_by_id.return_value = None

    with pytest.raises(EntityNotFound) as exc_info:
        await book_service.get_by_id(1)


async def test_get_all_success(
    book_service: BookService,
    mock_books: list[BookResponse]
):
    book_service.repository.get_all.return_value = mock_books[:2]

    fetched = await book_service.get_all()

    assert len(fetched) == 2
    titles = [book.title for book in mock_books[:2]]
    for book in fetched:
        assert book.title in titles


async def test_get_all_empty(book_service: BookService):
    book_service.repository.get_all.return_value = []

    fetched = await book_service.get_all()

    assert fetched == []


async def test_update_success(
    book_service: BookService,
    mock_publishers: list[PublisherResponse],
    mock_authors: list[AuthorResponse],
    mock_books: list[BookResponse],
    update_data: BookUpdate
):
    book_service.publisher_repository.get_by_id.return_value = (
        mock_publishers[2]
    )
    book_service.author_repository.get_by_ids.return_value = mock_authors[1:]
    book_service.repository.update.return_value = mock_books[2]

    updated = await book_service.update(1, update_data)

    assert updated.id == mock_books[2].id
    assert updated.title == mock_books[2].title


async def test_update_no_fields(book_service: BookService):
    with pytest.raises(NoFieldsToUpdate) as exc_info:
        await book_service.update(1, BookUpdate())


async def test_update_not_found(
    book_service: BookService,
    update_data: BookUpdate
):
    book_service.repository.update.return_value = None

    with pytest.raises(EntityNotFound) as exc_info:
        await book_service.update(1, update_data)


async def test_delete_success(book_service: BookService):
    book_service.repository.delete.return_value = True

    await book_service.delete(1)


async def test_delete_not_found(book_service: BookService):
    book_service.repository.delete.return_value = False

    with pytest.raises(EntityNotFound) as exc_info:
        await book_service.delete(1)
