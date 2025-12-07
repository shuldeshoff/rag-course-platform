# RAG Service

FastAPI сервис для обработки RAG запросов с YandexGPT.

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn app.main:app --reload
```

## Структура

- `app/` - основной код приложения
- `tests/` - тесты
- `alembic/` - миграции БД

