import pytest

from app.schemas import AuthorCreate, AuthorUpdate
from app.repositories import AuthorRepository

@pytest.fixture
def author_repository(db):
    return AuthorRepository(db)


@pytest.fixture
def create_data():
    return [
        AuthorCreate(name="Author One"),
        AuthorCreate(name="Author Two")
    ]


@pytest.fixture
def update_data():
    return AuthorUpdate(name="Author Three")


async def test_create_success(
    author_repository: AuthorRepository,
    create_data: list[AuthorCreate]
):
    created = await author_repository.create(create_data[0])

    assert created is not None
    assert created.id is not None
    assert created.created_at is not None
    assert created.updated_at is not None
    assert created.name == create_data[0].name


async def test_get_by_id_success(
    author_repository: AuthorRepository,
    create_data: list[AuthorCreate]
):
    created = await author_repository.create(create_data[0])

    fetched = await author_repository.get_by_id(created.id)
    
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.name == created.name


async def test_get_by_id_not_found(author_repository: AuthorRepository):
    fetched = await author_repository.get_by_id(1)

    assert fetched is None


async def test_get_all_with_data(
    author_repository: AuthorRepository,
    create_data: list[AuthorCreate]
):
    names = [author.name for author in create_data]
    for cd in create_data:
        await author_repository.create(cd)

    fetched = await author_repository.get_all()

    assert len(fetched) == 2
    for author in fetched:
        assert author.name in names


async def test_get_all_empty(author_repository: AuthorRepository):
    fetched = await author_repository.get_all()

    assert len(fetched) == 0
    assert fetched == []


async def test_update_success(
    author_repository: AuthorRepository,
    create_data: list[AuthorCreate],
    update_data: AuthorUpdate
):
    created = await author_repository.create(create_data[0])

    updated = await author_repository.update(created.id, update_data)

    assert updated is not None
    assert updated.id == created.id
    assert updated.created_at == created.created_at
    assert updated.updated_at >= created.updated_at
    assert updated.name == update_data.name


async def test_update_not_found(
    author_repository: AuthorRepository, update_data: AuthorUpdate
):
    updated = await author_repository.update(1, update_data)

    assert updated is None


async def test_delete_success(
    author_repository: AuthorRepository,
    create_data: AuthorCreate
):
    created = await author_repository.create(create_data[0])

    deleted = await author_repository.delete(created.id)

    assert deleted is True

    fetched = await author_repository.get_by_id(created.id)

    assert fetched is None


async def test_delete_not_found(author_repository: AuthorRepository):
    deleted = await author_repository.delete(1)

    assert deleted is False
