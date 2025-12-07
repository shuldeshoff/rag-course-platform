# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-12-07

### Added

#### RAG Service
- ✅ FastAPI application with full REST API
- ✅ RAG Pipeline: Embedder → Retriever → Generator
- ✅ Qdrant vector database integration
- ✅ YandexGPT API integration
- ✅ PostgreSQL for metadata and logs
- ✅ Redis caching and rate limiting
- ✅ Bearer token authentication
- ✅ Structured logging (structlog)
- ✅ Input validation and sanitization
- ✅ Document parsers (PDF, DOCX, TXT)
- ✅ Intelligent chunking strategies
- ✅ Admin API for indexing
- ✅ CLI tool for batch indexing
- ✅ Docker Compose setup
- ✅ Health checks and monitoring

#### Moodle Plugin
- ✅ Block plugin `block_aiassistant`
- ✅ Chat interface with AJAX
- ✅ Admin settings (URL, token, timeouts)
- ✅ PHP API client
- ✅ Database logging
- ✅ Multilingual support (EN/RU)
- ✅ Responsive CSS design
- ✅ Error handling
- ✅ Capability-based permissions

#### Course Content
- ✅ Module 1: LLM Basics - transformers, tokens, prompts
- ✅ Module 2: RAG Concept - architecture, vs fine-tuning
- ✅ Module 3: Vector Databases - Qdrant, metrics, HNSW
- ✅ Module 4: Data Preparation - parsing, chunking
- ✅ Module 5: Retrieval - semantic search, reranking
- ✅ Module 6: YandexGPT - API, parameters, prompts
- ✅ Module 7: Service Architecture - FastAPI, production
- ✅ Module 8: Final Project - requirements, criteria

#### Documentation
- ✅ Technical specification (1700+ lines)
- ✅ Development roadmap (19 weeks, 10 stages)
- ✅ Technology stack overview
- ✅ Project structure documentation
- ✅ Deployment guide
- ✅ Quick start guide
- ✅ Comprehensive README

#### Infrastructure
- ✅ Docker containerization
- ✅ Docker Compose orchestration
- ✅ Multi-service architecture
- ✅ Production-ready configuration
- ✅ Nginx reverse proxy setup
- ✅ SSL/TLS support

### Technical Details

**Performance:**
- Response time: < 5 seconds (95th percentile)
- Concurrent requests: up to 50
- Vector search: < 100ms
- Caching: 30 min TTL

**Security:**
- API token authentication
- Rate limiting: 10 req/min per user
- Input validation (XSS, SQL injection protection)
- HTTPS support
- CORS configuration

**Scalability:**
- Horizontal scaling ready
- Async processing
- Redis caching layer
- Connection pooling

### Testing
- Unit tests for RAG pipeline
- Integration tests for API
- Moodle plugin compatibility tests
- Load testing ready

### Known Limitations
- YandexGPT API quota: 20 req/min
- Single-language embeddings (multilingual-e5-large)
- Max chunk size: 500 characters (configurable)

## [Unreleased]

### Planned Features
- Telegram bot integration
- Voice input/output
- Multi-course support
- Advanced analytics dashboard
- A/B testing framework
- Mobile application

---

[1.0.0]: https://github.com/shuldeshoff/rag-course-platform/releases/tag/v1.0.0

