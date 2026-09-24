from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Author, Publisher
from app.schemas import BookCreate, BookUpdate
from app.repositories import BookRepository


@pytest.fixture
async def create_relations(db: AsyncSession):
    publishers = [
        Publisher(name="Publisher One"),
        Publisher(name="Publisher Two"),
        Publisher(name="Publisher Three")
    ]
    authors = [
        Author(name="Author One"),
        Author(name="Author Two"),
        Author(name="Author Three")
    ]
    db.add_all(publishers)
    db.add_all(authors)
    await db.commit()
    return authors, publishers


@pytest.fixture
def book_repository(db):
    return BookRepository(db)


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
    create_relations,
    book_repository: BookRepository,
    create_data: list[BookCreate]
):
    created = await book_repository.create(create_data[0])

    assert created is not None
    assert created.id is not None
    assert created.created_at is not None
    assert created.updated_at is not None
    assert created.title == create_data[0].title
    assert created.publication_date == create_data[0].publication_date
    assert created.isbn == create_data[0].isbn
    assert created.publisher_id == create_data[0].publisher_id


async def test_get_by_id_succes(
    create_relations,
    book_repository: BookRepository,
    create_data: list[BookCreate]
):
    created = await book_repository.create(create_data[0])

    fetched = await book_repository.get_by_id(created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.title == created.title
    assert fetched.publisher is not None
    assert fetched.publisher.id == created.publisher_id
    assert fetched.authors is not None
    assert {author.id for author in fetched.authors} == set(
        create_data[0].author_ids
    )


async def test_get_by_id_not_found(book_repository: BookRepository):
    fetched = await book_repository.get_by_id(1)

    assert fetched is None


async def test_get_all_with_data(
    create_relations,
    book_repository: BookRepository,
    create_data: list[BookCreate]
):
    titles = [book.title for book in create_data]
    for cd in create_data:
        await book_repository.create(cd)

    fetched = await book_repository.get_all()

    assert len(fetched) == 2
    for book in fetched:
        assert book.title in titles


async def test_get_all_empty(book_repository: BookRepository):
    fetched = await book_repository.get_all()

    assert len(fetched) == 0
    assert fetched == []


async def test_update_success(
    create_relations,
    book_repository: BookRepository,
    create_data: list[BookCreate],
    update_data: BookUpdate
):
    created = await book_repository.create(create_data[0])

    updated = await book_repository.update(created.id, update_data)

    assert updated is not None
    assert updated.id == created.id
    assert updated.created_at == created.created_at
    assert updated.updated_at >= created.updated_at
    assert updated.title == update_data.title


async def test_update_not_found(
    book_repository: BookRepository, update_data: BookUpdate
):
    updated = await book_repository.update(1, update_data)

    assert updated is None


async def test_delete_success(
    create_relations,
    book_repository: BookRepository,
    create_data: BookCreate
):
    created = await book_repository.create(create_data[0])

    deleted = await book_repository.delete(created.id)

    assert deleted is True

    fetched = await book_repository.get_by_id(created.id)

    assert fetched is None


async def test_delete_not_found(book_repository: BookRepository):
    deleted = await book_repository.delete(1)

    assert deleted is False
