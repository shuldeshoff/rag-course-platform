# Структура проекта

## RAG Service

```
rag-service/
├── app/
│   ├── main.py                 # FastAPI приложение
│   ├── config.py               # Настройки
│   ├── models/
│   │   ├── request.py         # Модели запросов
│   │   ├── response.py        # Модели ответов
│   │   └── database.py        # SQLAlchemy модели
│   ├── api/
│   │   ├── auth.py            # Авторизация
│   │   ├── ask.py             # Endpoint /ask
│   │   └── admin.py           # Admin endpoints
│   ├── services/
│   │   ├── embedder.py        # Эмбеддинги
│   │   ├── retriever.py       # Поиск
│   │   ├── generator.py       # YandexGPT
│   │   └── indexer.py         # Индексация
│   ├── database/
│   │   ├── db.py              # Connection
│   │   └── crud.py            # CRUD
│   └── utils/
│       ├── logger.py
│       ├── parsers.py
│       └── validators.py
├── alembic/                    # Миграции БД
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Moodle Plugin

```
moodle-block-aiassistant/
├── version.php                 # Версия
├── block_aiassistant.php       # Основной класс
├── settings.php                # Настройки
├── db/
│   ├── access.php             # Права
│   └── install.xml            # Схема БД
├── lang/
│   ├── en/
│   │   └── block_aiassistant.php
│   └── ru/
│       └── block_aiassistant.php
├── classes/
│   ├── api_client.php         # HTTP клиент
│   ├── logger.php             # Логи
│   └── output/
│       └── renderer.php
├── styles.css
├── amd/
│   └── src/
│       └── chat.js            # JavaScript
└── templates/
    └── chat_interface.mustache
```

## База данных

### PostgreSQL (RAG Service)

**requests_log** - логи запросов
**indexed_documents** - индексированные документы

### Moodle DB

**mdl_block_aiassistant_logs** - логи из Moodle

## Векторное хранилище

**Qdrant collection:** `course_materials`
- course_id (filter)
- content (payload)
- source (payload)
- metadata (payload)

## Зависимости

**Python:**
- fastapi
- uvicorn
- langchain
- sentence-transformers
- qdrant-client
- sqlalchemy
- pydantic
- yandexcloud
- pypdf2
- python-docx

**PHP:**
- Moodle API (встроенное)

**Инфраструктура:**
- Docker + Docker Compose
- PostgreSQL 15
- Qdrant 1.7+
- Redis 7 (кэширование)
- Nginx (reverse proxy)

