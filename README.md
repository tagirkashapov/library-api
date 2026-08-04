# Library API

Учебный REST API для управления библиотекой.

## Возможности

- Создавать книги
- Получать книги
- Обновлять книги
- Удалять книги

## Стек технологий

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite

## Структура проекта

```text
library-api/
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

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/books` | Получить список всех книг |
| GET | `/books/{id}` | Получить книгу по id |
| POST | `/books` | Создать книгу |
| PATCH | `/books/{id}` | Обновить данные книги по id |
| DELETE | `/books/{id}` | Удалить книгу по id |

## Изменения

- Вместо оперативной памяти для хранения данных используется SQLite, что позволяет хранить данные постоянно
- В качестве ORM используется SQLAlchemy
- Организована слоистая архитектура c разделением ответственности

## Планы по развитию

- Нормализовать базу данных
- Добавить миграции Alembic
