# Технологический стек

## Backend (RAG Service)

**Язык:** Python 3.10+

**Фреймворк:** FastAPI + Uvicorn

**ML/NLP:**
- LangChain - orchestration
- sentence-transformers - эмбеддинги
- Модель: intfloat/multilingual-e5-large

**База данных:**
- PostgreSQL 15 - метаданные
- Qdrant 1.7+ - векторное хранилище

**LLM:** YandexGPT API

**Кэш:** Redis 7

**ORM:** SQLAlchemy 2.0 + Alembic

---

## Frontend (Moodle Plugin)

**Backend:** PHP 7.4+ (Moodle API)

**Frontend:** Vanilla JavaScript (ES6+) + CSS3

**Шаблоны:** Mustache

---

## Инфраструктура

**Контейнеризация:** Docker + Docker Compose

**Веб-сервер:** Nginx (reverse proxy)

**SSL:** Let's Encrypt

**Мониторинг:** 
- Prometheus (метрики)
- structlog (логи)

---

## DevOps

**CI/CD:** GitHub Actions

**Развертывание:** Docker

---

## Требования к серверу

**Минимум:**
- 4 CPU / 8 GB RAM / 50 GB SSD
- Ubuntu 22.04 LTS

**Рекомендуется:**
- 8 CPU / 16 GB RAM / 100 GB NVMe

