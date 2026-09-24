from unittest.mock import AsyncMock
from datetime import datetime

import pytest

from app.core import EntityNotFound, NoFieldsToUpdate
from app.schemas import PublisherResponse, PublisherCreate, PublisherUpdate
from app.services import PublisherService


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.commit = AsyncMock()
    return db


@pytest.fixture
def publisher_service(mock_db):
    service = PublisherService(mock_db)
    service.repository = AsyncMock()
    service.repository.model.__name__ = "Publisher"
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
        PublisherCreate(name="Publisher One"),
        PublisherCreate(name="Publisher Two"),
    ]


@pytest.fixture
def update_data():
    return PublisherUpdate(name="Publisher Three")


async def test_create_success(
    publisher_service: PublisherService,
    mock_publishers: list[PublisherResponse],
    create_data: list[PublisherCreate]
):
    publisher_service.repository.create.return_value = mock_publishers[0]

    created = await publisher_service.create(create_data[0])

    assert created.id == mock_publishers[0].id
    assert created.created_at == mock_publishers[0].created_at
    assert created.updated_at == mock_publishers[0].updated_at
    assert created.name == mock_publishers[0].name


async def test_get_by_id_success(
    publisher_service: PublisherService,
    mock_publishers: list[PublisherResponse]
):
    publisher_service.repository.get_by_id.return_value = mock_publishers[0]

    fetched = await publisher_service.get_by_id(1)

    assert fetched.id == mock_publishers[0].id
    assert fetched.name == mock_publishers[0].name


async def test_get_by_id_not_found(publisher_service: PublisherService):
    publisher_service.repository.get_by_id.return_value = None

    with pytest.raises(EntityNotFound) as exc_info:
        await publisher_service.get_by_id(1)


async def test_get_all_success(
    publisher_service: PublisherService,
    mock_publishers: list[PublisherResponse]
):
    publisher_service.repository.get_all.return_value = mock_publishers[:2]

    fetched = await publisher_service.get_all()

    assert len(fetched) == 2
    names = [publisher.name for publisher in mock_publishers[:2]]
    for publisher in fetched:
        assert publisher.name in names


async def test_get_all_empty(publisher_service: PublisherService):
    publisher_service.repository.get_all.return_value = []

    fetched = await publisher_service.get_all()

    assert fetched == []


async def test_update_success(
    publisher_service: PublisherService,
    mock_publishers: list[PublisherResponse],
    update_data: PublisherUpdate
):
    publisher_service.repository.update.return_value = mock_publishers[2]

    updated = await publisher_service.update(1, update_data)

    assert updated.id == mock_publishers[2].id
    assert updated.name == mock_publishers[2].name


async def test_update_no_fields(publisher_service: PublisherService):
    with pytest.raises(NoFieldsToUpdate) as exc_info:
        await publisher_service.update(1, PublisherUpdate())


async def test_update_not_found(
    publisher_service: PublisherService,
    update_data: PublisherUpdate
):
    publisher_service.repository.update.return_value = None

    with pytest.raises(EntityNotFound) as exc_info:
        await publisher_service.update(1, update_data)


async def test_delete_success(publisher_service: PublisherService):
    publisher_service.repository.delete.return_value = True

    await publisher_service.delete(1)


async def test_delete_not_found(publisher_service: PublisherService):
    publisher_service.repository.delete.return_value = False

    with pytest.raises(EntityNotFound) as exc_info:
        await publisher_service.delete(1)
