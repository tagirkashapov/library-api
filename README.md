# Library API

Учебный REST API для управления библиотекой.

## Возможности

API дает возможность работать с тремя сущностями:
- Издательства
- Авторы
- Книги (M:1 связь с издательствами, M:M связь с авторами)

Эти сущности можно:
- Создавать
- Получать
- Обновлять
- Удалять

## Стек технологий

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- SQLite

## Структура проекта

```text
library-api/
├── alembic/
│   ├── versions/
│   │   └── ...
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── api/
│   │   ├── books.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── db/
│   │   ├── base.py
│   │   └── db.py
│   ├── models/
│   │   └── book.py
│   ├── repositories/
│   │   └── book.py
│   ├── schemas/
│   │   └── book.py
│   ├── services/
│   │   └── book.py
│   └── main.py
├── .env.example
├── .gitignore
├── alembic.ini
├── LICENSE
├── README.md
└── requirements.txt
```

## Установка и запуск

```bash
git clone <URL_репозитория>

cd <папка_проекта>

python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

После запуска Swagger доступен по адресу:

```text
http://127.0.0.1:8000/docs
```

## API

### Издательства

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/publishers` | Получить список всех издательств |
| GET | `/publishers/{id}` | Получить издательство по id |
| POST | `/publishers` | Создать издательство |
| PATCH | `/publishers/{id}` | Обновить данные издательства по id |
| DELETE | `/publishers/{id}` | Удалить издательство по id |

### Авторы

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/authors` | Получить список всех авторов |
| GET | `/authors/{id}` | Получить автора по id |
| POST | `/authors` | Создать автора |
| PATCH | `/authors/{id}` | Обновить данные автора по id |
| DELETE | `/authors/{id}` | Удалить автора по id |

### Книги

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/books` | Получить список всех книг |
| GET | `/books/{id}` | Получить книгу по id |
| POST | `/books` | Создать книгу |
| PATCH | `/books/{id}` | Обновить данные книги по id |
| DELETE | `/books/{id}` | Удалить книгу по id |

## Изменения

- Нормализована база данных
- Добавлена логика работы с авторами и издательствами
- Изменена логика работы с книгами
- Добавлены миграции Alembic

## Планы по развитию

- Добавить Docker
- Использовать PostgreSQL для хранения данных вместо SQLite
