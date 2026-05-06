# Contacts API

REST API для зберігання та управління контактами на `FastAPI` з використанням `SQLAlchemy` та `PostgreSQL`.

## Можливості

- створення нового контакту
- отримання списку всіх контактів
- отримання контакту за `id`
- оновлення контакту
- видалення контакту
- пошук контактів за `first_name`, `last_name`, `email`
- отримання контактів з днями народження на найближчі 7 днів
- Swagger документація
- запуск через `Docker Compose`
- тестові seed-дані для швидкої перевірки API

## Структура даних контакту

Контакт містить такі поля:

- `first_name`
- `last_name`
- `email`
- `phone`
- `birthday`
- `additional_data`

## Запуск проєкту

### Варіант 1. Через Docker Compose

Основний спосіб запуску:

```bash
make build
```

Ця команда:

- збирає контейнери
- запускає `FastAPI`, `PostgreSQL` і `PgAdmin`
- додає тестові записи в базу

Корисні команди:

```bash
make run
make stop
make restart
make logs
make seed-docker
```

### Варіант 2. Локально

Створити та активувати віртуальне середовище, потім встановити залежності:

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Для додавання тестових записів локально:

```bash
make seed
```

## Змінні середовища

Файл `.env`:

```env
APP_NAME=Contacts API
POSTGRES_DB=contacts_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Опис змінних:

- `APP_NAME` — назва застосунку у Swagger
- `POSTGRES_DB` — назва бази даних
- `POSTGRES_USER` — користувач PostgreSQL
- `POSTGRES_PASSWORD` — пароль PostgreSQL
- `POSTGRES_HOST` — хост PostgreSQL для локального запуску
- `POSTGRES_PORT` — порт PostgreSQL

Примітка: у Docker для сервісу `web` значення `POSTGRES_HOST` перевизначається на `postgres`.

## Swagger

Swagger документація доступна за адресою:

- `http://127.0.0.1:8000/docs`

OpenAPI schema:

- `http://127.0.0.1:8000/openapi.json`

Документація Swagger перевірена: endpoint `/docs` відповідає зі статусом `200`.

## PgAdmin

PgAdmin доступний за адресою:

- `http://127.0.0.1:8080`

Дані для входу:

- email: `admin@example.com`
- password: `admin123`

Для підключення до PostgreSQL у PgAdmin використовуйте:

- host: `postgres`
- port: `5432`
- database: `contacts_db`
- username: `postgres`
- password: `postgres`

## Endpoint-и API

### Базові endpoint-и

- `GET /` — перевірка, що API працює
- `POST /api/contacts/` — створити контакт
- `GET /api/contacts/` — отримати всі контакти
- `GET /api/contacts/{contact_id}` — отримати контакт за `id`
- `PUT /api/contacts/{contact_id}` — оновити контакт
- `DELETE /api/contacts/{contact_id}` — видалити контакт

### Додаткові endpoint-и

- `GET /api/contacts/?first_name=...`
- `GET /api/contacts/?last_name=...`
- `GET /api/contacts/?email=...`
- `GET /api/contacts/upcoming-birthdays`

## Приклади запитів

### Створити контакт

```bash
curl -X POST "http://127.0.0.1:8000/api/contacts/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"first_name\": \"Ivan\",
    \"last_name\": \"Franko\",
    \"email\": \"ivan.franko@example.com\",
    \"phone\": \"+380501234567\",
    \"birthday\": \"1990-08-27\",
    \"additional_data\": \"Test contact\"
  }"
```

### Отримати всі контакти

```bash
curl -X GET "http://127.0.0.1:8000/api/contacts/"
```

### Пошук за email

```bash
curl -X GET "http://127.0.0.1:8000/api/contacts/?email=franko%40example.com"
```

### Найближчі дні народження

```bash
curl -X GET "http://127.0.0.1:8000/api/contacts/upcoming-birthdays"
```

## Тестові дані

Seed-скрипт знаходиться тут:

- [seed.py](src/database/seed.py)

Він додає кілька контактів для швидкої перевірки API.
