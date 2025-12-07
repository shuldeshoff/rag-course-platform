# Модуль 7: Архитектура RAG-сервиса

## Цели модуля
- Спроектировать RAG API
- Реализовать на FastAPI
- Добавить кэширование и оптимизацию
- Настроить мониторинг
- Подготовить к деплою

## Лекция: Production RAG Service

### 1. Архитектура сервиса

```
┌─────────────────────────────────────────┐
│           API Layer (FastAPI)           │
│  /ask /index /health /admin/stats       │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         Business Logic Layer            │
│  ┌─────────────┐  ┌──────────────────┐ │
│  │ RAG Pipeline│  │  Document        │ │
│  │             │  │  Indexer         │ │
│  └─────────────┘  └──────────────────┘ │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│          Data Layer                     │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐│
│  │PostgreSQL│ │  Qdrant  │ │  Redis  ││
│  │(Metadata)│ │(Vectors) │ │(Cache)  ││
│  └──────────┘ └──────────┘ └─────────┘│
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         External Services               │
│           YandexGPT API                 │
└─────────────────────────────────────────┘
```

### 2. FastAPI приложение

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_services()
    yield
    # Shutdown
    await cleanup_services()

app = FastAPI(
    title="RAG Service API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Routes
from app.api import ask, admin, health

app.include_router(ask.router)
app.include_router(admin.router)
app.include_router(health.router)
```

### 3. Dependency Injection

```python
from fastapi import Depends

# Зависимости
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_rag_pipeline():
    return RAGPipeline(
        retriever=retriever_service,
        generator=generator_service
    )

# Использование
@app.post("/ask")
async def ask(
    request: AskRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline),
    db: Session = Depends(get_db)
):
    answer = await pipeline.process(request.question)
    log_request(db, request, answer)
    return answer
```

### 4. Асинхронность

```python
import asyncio

class RAGPipeline:
    async def process(self, question, course_id):
        # Параллельный поиск в нескольких индексах
        search_tasks = [
            self.search_main_docs(question, course_id),
            self.search_qa_pairs(question, course_id)
        ]
        
        results = await asyncio.gather(*search_tasks)
        all_chunks = self.merge_results(results)
        
        # Генерация
        answer = await self.generator.generate(question, all_chunks)
        
        return answer
```

### 5. Кэширование

```python
from redis import asyncio as aioredis
import hashlib

class CacheService:
    def __init__(self):
        self.redis = aioredis.from_url("redis://localhost")
    
    def make_key(self, *args):
        data = json.dumps(args)
        return hashlib.md5(data.encode()).hexdigest()
    
    async def get(self, key):
        value = await self.redis.get(key)
        return json.loads(value) if value else None
    
    async def set(self, key, value, ttl=1800):
        await self.redis.setex(key, ttl, json.dumps(value))

# Декоратор для кэширования
def cached(ttl=1800):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            key = cache.make_key(func.__name__, args, kwargs)
            
            # Проверить кэш
            cached_value = await cache.get(key)
            if cached_value:
                return cached_value
            
            # Вычислить
            result = await func(*args, **kwargs)
            
            # Сохранить в кэш
            await cache.set(key, result, ttl)
            
            return result
        return wrapper
    return decorator

@cached(ttl=3600)
async def expensive_operation(query):
    # Долгая операция
    pass
```

### 6. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/ask")
@limiter.limit("10/minute")
async def ask(request: Request, data: AskRequest):
    return await process_ask(data)
```

### 7. Мониторинг и логирование

```python
import structlog
from prometheus_client import Counter, Histogram

# Метрики
request_count = Counter('rag_requests_total', 'Total requests')
request_duration = Histogram('rag_request_duration_seconds', 'Request duration')
cache_hits = Counter('rag_cache_hits_total', 'Cache hits')

# Логирование
logger = structlog.get_logger()

@app.post("/ask")
async def ask(request: AskRequest):
    request_count.inc()
    
    with request_duration.time():
        logger.info("ask_request", 
                   user_id=request.user_id,
                   course_id=request.course_id)
        
        try:
            answer = await pipeline.process(request)
            
            logger.info("ask_success",
                       response_time=answer.response_time_ms)
            
            return answer
            
        except Exception as e:
            logger.error("ask_error", error=str(e))
            raise
```

### 8. Обработка ошибок

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class RAGServiceError(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code

@app.exception_handler(RAGServiceError)
async def rag_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": exc.message,
            "code": exc.code
        }
    )

@app.exception_handler(HTTPException)
async def http_error_handler(request, exc):
    logger.error("http_error",
                status_code=exc.status_code,
                detail=exc.detail)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
```

### 9. Конфигурация

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TOKEN: str
    
    # Database
    POSTGRES_URL: str
    QDRANT_URL: str
    REDIS_URL: str
    
    # YandexGPT
    YANDEX_API_KEY: str
    YANDEX_FOLDER_ID: str
    
    # Performance
    MAX_WORKERS: int = 4
    REQUEST_TIMEOUT: int = 30
    CACHE_TTL: int = 1800
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 10. Тестирование

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_ask_endpoint():
    response = client.post(
        "/ask",
        json={
            "user_id": 1,
            "course_id": 1,
            "question": "Что такое RAG?"
        },
        headers={"Authorization": f"Bearer {API_TOKEN}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 0

def test_rate_limiting():
    for _ in range(15):
        response = client.post("/ask", json={...})
    
    assert response.status_code == 429
```

## Практическое задание

1. Создать FastAPI приложение с полной структурой
2. Реализовать все endpoints
3. Добавить кэширование через Redis
4. Настроить логирование и метрики
5. Написать тесты
6. Подготовить Docker Compose

## Тест

1. Зачем нужен lifespan в FastAPI?
2. Что такое dependency injection?
3. Как работает кэширование в Redis?
4. Какие метрики важны для RAG сервиса?
5. Как правильно обрабатывать ошибки в API?

