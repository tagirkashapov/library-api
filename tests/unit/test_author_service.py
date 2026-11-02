from unittest.mock import AsyncMock
from datetime import datetime

import pytest

from app.core import EntityNotFound, NoFieldsToUpdate
from app.schemas import AuthorResponse, AuthorCreate, AuthorUpdate
from app.services import AuthorService


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    return db


@pytest.fixture
def author_service(mock_db):
    service = AuthorService(mock_db)
    service.repository = AsyncMock()
    service.repository.model.__name__ = "Author"
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
        AuthorCreate(name="Author One"),
        AuthorCreate(name="Author Two"),
    ]


@pytest.fixture
def update_data():
    return AuthorUpdate(name="Author Three")


async def test_create_success(
    author_service: AuthorService,
    mock_authors: list[AuthorResponse],
    create_data: list[AuthorCreate]
):
    author_service.repository.create.return_value = mock_authors[0]

    created = await author_service.create(create_data[0])

    assert created.id == mock_authors[0].id
    assert created.created_at == mock_authors[0].created_at
    assert created.updated_at == mock_authors[0].updated_at
    assert created.name == mock_authors[0].name


async def test_get_by_id_success(
    author_service: AuthorService,
    mock_authors: list[AuthorResponse]
):
    author_service.repository.get_by_id.return_value = mock_authors[0]

    fetched = await author_service.get_by_id(1)

    assert fetched.id == mock_authors[0].id
    assert fetched.name == mock_authors[0].name


async def test_get_by_id_not_found(author_service: AuthorService):
    author_service.repository.get_by_id.return_value = None

    with pytest.raises(EntityNotFound) as exc_info:
        await author_service.get_by_id(1)


async def test_get_all_success(
    author_service: AuthorService,
    mock_authors: list[AuthorResponse]
):
    author_service.repository.get_all.return_value = mock_authors[:2]

    fetched = await author_service.get_all()

    assert len(fetched) == 2
    names = [author.name for author in mock_authors[:2]]
    for author in fetched:
        assert author.name in names


async def test_get_all_empty(author_service: AuthorService):
    author_service.repository.get_all.return_value = []

    fetched = await author_service.get_all()

    assert fetched == []


async def test_update_success(
    author_service: AuthorService,
    mock_authors: list[AuthorResponse],
    update_data: AuthorUpdate
):
    author_service.repository.update.return_value = mock_authors[2]

    updated = await author_service.update(1, update_data)

    assert updated.id == mock_authors[2].id
    assert updated.name == mock_authors[2].name


async def test_update_no_fields(author_service: AuthorService):
    with pytest.raises(NoFieldsToUpdate) as exc_info:
        await author_service.update(1, AuthorUpdate())


async def test_update_not_found(
    author_service: AuthorService,
    update_data: AuthorUpdate
):
    author_service.repository.update.return_value = None

    with pytest.raises(EntityNotFound) as exc_info:
        await author_service.update(1, update_data)


async def test_delete_success(author_service: AuthorService):
    author_service.repository.delete.return_value = True

    await author_service.delete(1)


async def test_delete_not_found(author_service: AuthorService):
    author_service.repository.delete.return_value = False

    with pytest.raises(EntityNotFound) as exc_info:
        await author_service.delete(1)
