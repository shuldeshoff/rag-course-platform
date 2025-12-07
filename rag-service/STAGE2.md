# Stage 2: RAG Pipeline - COMPLETE

## Реализовано

✅ **Embedder Service** - создание векторных представлений
- sentence-transformers
- intfloat/multilingual-e5-large model
- Batch processing support

✅ **Retriever Service** - семантический поиск
- Интеграция с Qdrant
- Фильтрация по course_id
- Top-K результаты

✅ **Generator Service** - генерация с контекстом
- RAG-оптимизированные промпты
- Интеграция с YandexGPT
- Контекстные материалы курса

✅ **RAG Pipeline** - полный процесс
- Retrieve → Generate → Response
- Автоматическая оркестрация
- Измерение времени ответа

## Тестирование

```bash
cd rag-service

# Запустить все сервисы
docker-compose up -d

# Подождать загрузки модели (~2 минуты)
docker-compose logs -f rag-service

# Тесты
pip install -r requirements-dev.txt
pytest tests/test_rag.py -v
```

## Пример использования

```bash
# 1. Добавить тестовые данные в Qdrant
curl -X POST http://localhost:8000/test-insert \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1,
    "content": "RAG (Retrieval-Augmented Generation) - это архитектура, которая улучшает ответы LLM через поиск релевантной информации.",
    "metadata": {"source": "Module 2", "page": 1}
  }'

# 2. Задать вопрос с RAG
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer your-secret-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "course_id": 1,
    "question": "Что такое RAG?"
  }'
```

## Архитектура RAG Pipeline

```
Question → Embedder → Vector
              ↓
Vector → Qdrant Search → Top-K Chunks
              ↓
Chunks + Question → Prompt Builder → Context Prompt
              ↓
Context Prompt → YandexGPT → Answer
```

## Следующий этап

**Этап 3: Индексация документов**
- Парсеры PDF/DOCX/TXT
- Chunking стратегии
- Admin API для загрузки
- CLI инструменты

