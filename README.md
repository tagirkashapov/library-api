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

## Структура проекта

```text
library-api/
├── app/
│   ├── main.py
│   └── schemas.py
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

## Примечание

Данные хранятся в оперативной памяти и очищаются после перезапуска приложения.

## Планы по развитию

- Вместо оперативной памяти для хранения данных использовать SQLite, что позволит хранить данные постоянно
- В качестве ORM использовать SQLAlchemy
- Организовать слоистую архитектуру с разделением ответственности
