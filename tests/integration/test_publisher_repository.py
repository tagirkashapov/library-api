import pytest

from app.schemas import PublisherCreate, PublisherUpdate
from app.repositories import PublisherRepository

@pytest.fixture
def publisher_repository(db):
    return PublisherRepository(db)


@pytest.fixture
def create_data():
    return [
        PublisherCreate(name="Publisher One"),
        PublisherCreate(name="Publisher Two")
    ]


@pytest.fixture
def update_data():
    return PublisherUpdate(name="Publisher Three")


async def test_create_success(
    publisher_repository: PublisherRepository,
    create_data: list[PublisherCreate]
):
    created = await publisher_repository.create(create_data[0])

    assert created is not None
    assert created.id is not None
    assert created.created_at is not None
    assert created.updated_at is not None
    assert created.name == create_data[0].name


async def test_get_by_id_success(
    publisher_repository: PublisherRepository,
    create_data: list[PublisherCreate]
):
    created = await publisher_repository.create(create_data[0])

    fetched = await publisher_repository.get_by_id(created.id)
    
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.name == created.name


async def test_get_by_id_not_found(publisher_repository: PublisherRepository):
    fetched = await publisher_repository.get_by_id(1)

    assert fetched is None


async def test_get_all_with_data(
    publisher_repository: PublisherRepository,
    create_data: list[PublisherCreate]
):
    names = [publisher.name for publisher in create_data]
    for cd in create_data:
        await publisher_repository.create(cd)

    fetched = await publisher_repository.get_all()

    assert len(fetched) == 2
    for publisher in fetched:
        assert publisher.name in names


async def test_get_all_empty(publisher_repository: PublisherRepository):
    fetched = await publisher_repository.get_all()

    assert len(fetched) == 0
    assert fetched == []


async def test_update_success(
    publisher_repository: PublisherRepository,
    create_data: list[PublisherCreate],
    update_data: PublisherUpdate
):
    created = await publisher_repository.create(create_data[0])

    updated = await publisher_repository.update(created.id, update_data)

    assert updated is not None
    assert updated.id == created.id
    assert updated.created_at == created.created_at
    assert updated.updated_at >= created.updated_at
    assert updated.name == update_data.name


async def test_update_not_found(
    publisher_repository: PublisherRepository, update_data: PublisherUpdate
):
    updated = await publisher_repository.update(1, update_data)

    assert updated is None


async def test_delete_success(
    publisher_repository: PublisherRepository,
    create_data: PublisherCreate
):
    created = await publisher_repository.create(create_data[0])

    deleted = await publisher_repository.delete(created.id)

    assert deleted is True

    fetched = await publisher_repository.get_by_id(created.id)

    assert fetched is None


async def test_delete_not_found(publisher_repository: PublisherRepository):
    deleted = await publisher_repository.delete(1)

    assert deleted is False
