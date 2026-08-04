from fastapi import FastAPI, status, HTTPException

from app.schemas import BookResponse, BookCreate, BookUpdate

app = FastAPI()

books: list[BookResponse] = []
counter = 1


def get_book_by_id(book_id: int) -> BookResponse:
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.get("/books", response_model=list[BookResponse], tags=["Books"])
def get_books() -> list[BookResponse]:
    """Получить список всех книг"""
    return books


@app.get("/books/{book_id}", response_model=BookResponse, tags=["Books"])
def get_book(book_id: int) -> BookResponse:
    """Получить книгу по id"""
    return get_book_by_id(book_id)


@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=BookResponse, tags=["Books"])
def create_book(book_create: BookCreate) -> BookResponse:
    """Создать книгу"""
    global counter
    new_book = BookResponse(
        id=counter,
        **book_create.model_dump(),
    )
    books.append(new_book)
    counter += 1
    return new_book


@app.patch("/books/{book_id}", response_model=BookResponse, tags=["Books"])
def update_book(book_id: int, book_update: BookUpdate) -> BookResponse:
    """Обновить данные книги по id"""
    book = get_book_by_id(book_id)
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
def delete_book(book_id: int) -> None:
    """Удалить книгу по id"""
    book = get_book_by_id(book_id)
    books.remove(book)
