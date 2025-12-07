# RAG Course Platform

Платформа для создания и проведения курсов с интеграцией RAG и YandexGPT в Moodle LMS.

## Описание

Проект включает учебный курс "Практический RAG и YandexGPT для начинающих" с интегрированным AI-ассистентом, который отвечает на вопросы студентов на основе материалов курса.

## Структура проекта

```
rag-course-platform/
├── docs/                  # Документация
├── rag-service/          # FastAPI RAG сервис
└── moodle-plugin/        # Moodle блок-плагин
```

## Технологический стек

**Backend:**
- Python 3.10+ / FastAPI
- PostgreSQL 15
- Qdrant (векторное хранилище)
- LangChain + sentence-transformers
- YandexGPT API

**Moodle Plugin:**
- PHP 7.4+
- JavaScript (ES6+)
- Mustache templates

## Быстрый старт

Документация по установке и настройке находится в папке `docs/`

## Roadmap

Проект находится в стадии разработки. План реализации: 19 недель, 10 этапов.

См. `docs/roadmap.md` для деталей.

## Лицензия

MIT

## Автор

Yuriy Shuldeshov - [GitHub](https://github.com/shuldeshoff)

