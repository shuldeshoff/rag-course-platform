# Базовая инфраструктура - Этап 1

## Запуск через Docker Compose

```bash
cd rag-service

# Создать .env файл
cp .env.example .env
# Отредактировать .env (установить токены)

# Запустить все сервисы
docker-compose up -d

# Проверить логи
docker-compose logs -f rag-service

# Остановить
docker-compose down
```

## Проверка работоспособности

```bash
# Health check
curl http://localhost:8000/health

# Тест Qdrant
curl http://localhost:8000/test-qdrant

# Тест YandexGPT (требует настройки API ключей)
curl http://localhost:8000/test-yandex

# Тест /ask endpoint
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer your-secret-token-here" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "course_id": 1, "question": "Что такое RAG?"}'
```

## Локальная разработка

```bash
cd rag-service

# Создать venv
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Запустить отдельно PostgreSQL и Qdrant через Docker
docker-compose up -d postgres qdrant

# Запустить FastAPI локально
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Документация

После запуска доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Что реализовано

✅ FastAPI приложение с основными endpoints  
✅ Подключение к PostgreSQL  
✅ Интеграция с Qdrant  
✅ Интеграция с YandexGPT API  
✅ Аутентификация по Bearer token  
✅ Health check со статусом всех сервисов  
✅ Docker Compose для всей инфраструктуры  
✅ Базовые модели данных

## Следующий этап

Этап 2: RAG Pipeline - реализация embeddings, retrieval и полного RAG процесса

