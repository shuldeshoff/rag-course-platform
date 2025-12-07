# Stage 3: Document Indexing - COMPLETE

## Реализовано

✅ **Document Parsers**
- PDF parser (PyPDF2)
- DOCX parser (python-docx)
- TXT parser
- Text cleaning and normalization

✅ **Chunking Strategies**
- Sentence-based chunking
- Character-based chunking with overlap
- Smart boundary detection
- Configurable chunk size and overlap

✅ **Indexer Service**
- Document indexing pipeline
- Batch embedding creation
- Qdrant storage integration
- Metadata management

✅ **Admin API**
- POST /admin/index/file - загрузка файлов
- POST /admin/index/text - индексация текста
- GET /admin/stats/{course_id} - статистика

✅ **CLI Tools**
- cli_indexer.py для индексации из командной строки
- Поддержка файлов и директорий

✅ **Test Data**
- Примеры текстов по RAG и YandexGPT

## Использование

### Через API

```bash
# Индексация файла
curl -X POST http://localhost:8000/admin/index/file \
  -H "Authorization: Bearer your-token" \
  -F "course_id=1" \
  -F "title=RAG Basics" \
  -F "file=@document.pdf"

# Индексация текста
curl -X POST http://localhost:8000/admin/index/text \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1,
    "title": "RAG Introduction",
    "content": "RAG - это...",
    "metadata": {"module": 1}
  }'

# Статистика курса
curl http://localhost:8000/admin/stats/1 \
  -H "Authorization: Bearer your-token"
```

### Через CLI

```bash
# Индексация одного файла
python cli_indexer.py file course-materials/test-data/rag-basics.txt 1 "RAG Basics"

# Индексация всей папки
python cli_indexer.py dir course-materials/test-data 1
```

### Пример с тестовыми данными

```bash
cd rag-service

# Запустить сервисы
docker-compose up -d

# Дождаться загрузки модели
docker-compose logs -f rag-service

# Индексировать тестовые данные
python cli_indexer.py dir ../course-materials/test-data 1

# Протестировать RAG
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer your-secret-token-here" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "course_id": 1, "question": "Что такое RAG?"}'
```

## Chunking Configuration

В `.env` или `config.py`:

```
CHUNK_SIZE=500        # Размер чанка в символах
CHUNK_OVERLAP=50      # Перекрытие между чанками
```

## Поддерживаемые форматы

- ✅ PDF (.pdf)
- ✅ DOCX (.docx)
- ✅ TXT (.txt)

## Следующий этап

**Этап 4: Moodle Plugin**
- Структура плагина
- UI чата
- PHP API клиент
- AJAX обработка
- Настройки администратора

