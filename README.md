# RAG Course Platform

🚀 Полнофункциональная платформа для создания AI-курсов с интеграцией RAG и YandexGPT в Moodle LMS.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Moodle 3.9+](https://img.shields.io/badge/moodle-3.9+-orange.svg)](https://moodle.org/)

## 📖 О проекте

Полное решение для образовательной платформы с AI-ассистентом на базе RAG (Retrieval-Augmented Generation):

- ✅ **RAG-сервис** на FastAPI с YandexGPT
- ✅ **Moodle плагин** для интеграции ассистента  
- ✅ **Полный курс** "RAG и YandexGPT для начинающих" (8 модулей)
- ✅ **Production-ready** с кэшированием, rate limiting, мониторингом

## 🎯 Возможности

- 💬 AI-ассистент отвечает на вопросы по материалам курса
- 🔍 Семантический поиск с Qdrant
- 🤖 Интеграция YandexGPT API
- 📚 Готовый курс с 8 модулями и практическими заданиями
- 🔒 Безопасность: аутентификация, rate limiting, валидация
- ⚡ Производительность: Redis кэш, async, оптимизация
- 📊 Мониторинг: structured logging, метрики

## 🚀 Быстрый старт

### За 5 минут

```bash
# 1. Клонировать
git clone https://github.com/shuldeshoff/rag-course-platform.git
cd rag-course-platform

# 2. Настроить
cd rag-service
cp .env.example .env
# Добавить YANDEX_API_KEY и YANDEX_FOLDER_ID в .env

# 3. Запустить
docker-compose up -d

# 4. Проверить
curl http://localhost:8000/health

# 5. Индексировать материалы
python cli_indexer.py dir ../course-materials/test-data 1

# 6. Спросить
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer your-secret-token-here" \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"course_id":1,"question":"Что такое RAG?"}'
```

Подробнее: [DEPLOY.md](DEPLOY.md)

## 📁 Структура проекта

```
rag-course-platform/
├── rag-service/              # FastAPI RAG сервис
│   ├── app/
│   │   ├── api/             # REST API endpoints
│   │   ├── services/        # Бизнес-логика (RAG pipeline)
│   │   ├── models/          # Pydantic модели
│   │   ├── database/        # PostgreSQL
│   │   └── utils/           # Утилиты (cache, rate limit)
│   ├── tests/               # Тесты
│   ├── docker-compose.yml   # Docker окружение
│   └── cli_indexer.py       # CLI для индексации
│
├── moodle-plugin/           # Moodle блок-плагин
│   ├── block_aiassistant.php
│   ├── classes/             # PHP классы
│   ├── amd/src/             # JavaScript
│   ├── templates/           # Mustache
│   └── lang/                # Локализация (en/ru)
│
├── course-materials/        # Материалы курса
│   ├── module-1/            # Основы LLM
│   ├── module-2/            # Что такое RAG
│   ├── module-3/            # Векторные хранилища
│   ├── module-4/            # Подготовка данных
│   ├── module-5/            # Retrieval
│   ├── module-6/            # YandexGPT
│   ├── module-7/            # Архитектура
│   └── module-8/            # Финальный проект
│
└── docs/                    # Документация
    ├── technical-specification.md
    ├── roadmap.md
    ├── tech-stack.md
    └── project-structure.md
```

## 🛠️ Технологии

### Backend (RAG Service)
- **FastAPI** 0.104+ - async REST API
- **Python** 3.10+ 
- **Qdrant** - векторное хранилище
- **PostgreSQL** 15 - метаданные и логи
- **Redis** 7 - кэширование
- **sentence-transformers** - эмбеддинги (multilingual-e5-large)
- **YandexGPT** - генерация ответов
- **LangChain** - orchestration

### Frontend (Moodle Plugin)
- **PHP** 7.4+ (Moodle API)
- **JavaScript** ES6+ (AMD modules)
- **Mustache** - шаблоны
- **CSS3** - адаптивный дизайн

### Infrastructure
- **Docker** + Docker Compose
- **Nginx** - reverse proxy
- **Let's Encrypt** - SSL
- **structlog** - JSON logging
- **Prometheus** - метрики (опционально)

## 📚 Учебный курс

### 8 модулей (19 недель)

1. **Основы LLM** - трансформеры, токенизация, промпты
2. **Что такое RAG** - концепция, архитектура, vs fine-tuning
3. **Векторные хранилища** - Qdrant, метрики сходства, HNSW
4. **Подготовка данных** - парсинг, chunking, pipeline
5. **Retrieval** - semantic search, гибридный поиск, ре-ранжирование
6. **YandexGPT** - API, параметры, RAG-промпты, квоты
7. **Архитектура** - FastAPI, кэш, мониторинг, production
8. **Финальный проект** - полноценная RAG-система

Каждый модуль: лекции + практика + тесты + примеры кода

## 🔧 Требования

### Минимальные
- CPU: 4 ядра
- RAM: 8 GB
- Диск: 50 GB SSD
- OS: Ubuntu 22.04 LTS

### Рекомендуемые (production)
- CPU: 8 ядер
- RAM: 16 GB
- Диск: 100 GB NVMe SSD

### Для разработки
- Python 3.10+
- Docker + Docker Compose
- Moodle 3.9+ (для плагина)
- YandexGPT API ключ

## 📖 Документация

- [Quick Start](DEPLOY.md) - быстрый запуск и деплой
- [Technical Specification](docs/technical-specification.md) - детальное ТЗ
- [Roadmap](docs/roadmap.md) - план разработки
- [Tech Stack](docs/tech-stack.md) - технологии
- [RAG Service Setup](rag-service/SETUP.md) - настройка сервиса
- [Moodle Plugin](moodle-plugin/README.md) - установка плагина

## 🧪 Тестирование

```bash
cd rag-service

# Установить dev зависимости
pip install -r requirements-dev.txt

# Запустить тесты
pytest tests/ -v

# С покрытием
pytest tests/ --cov=app --cov-report=html
```

## 🤝 Вклад в проект

Мы приветствуем вклад в проект! 

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing`)
5. Откройте Pull Request

## 📊 Статус проекта

- ✅ Этап 1: Базовая инфраструктура
- ✅ Этап 2: RAG Pipeline  
- ✅ Этап 3: Индексация документов
- ✅ Этап 4: Moodle Plugin
- ✅ Этап 5: Безопасность и оптимизация
- ✅ Этапы 6-7: Контент курса (все 8 модулей)
- ✅ Этап 8: Документация и деплой
- 🚀 Готов к production!

## 📝 Лицензия

MIT License - см. [LICENSE](LICENSE)

## 👨‍💻 Автор

**Yuriy Shuldeshov**

- GitHub: [@shuldeshoff](https://github.com/shuldeshoff)
- LinkedIn: [in/shuldeshoff](https://linkedin.com/in/shuldeshoff)
- Website: [shuldeshov.pro](https://shuldeshov.pro)

## 🙏 Благодарности

- [YandexGPT](https://cloud.yandex.ru/services/yandexgpt) - LLM API
- [Qdrant](https://qdrant.tech/) - векторная БД
- [FastAPI](https://fastapi.tiangolo.com/) - web framework
- [Moodle](https://moodle.org/) - LMS платформа

## 📞 Поддержка

- 🐛 [Issues](https://github.com/shuldeshoff/rag-course-platform/issues)
- 💬 [Discussions](https://github.com/shuldeshoff/rag-course-platform/discussions)
- 📧 Email: support@example.com

---

⭐ Если проект был полезен, поставьте звезду!

