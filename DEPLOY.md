# RAG Course Platform - Quick Start Guide

## Быстрый старт (5 минут)

### 1. Клонировать репозиторий
```bash
git clone https://github.com/shuldeshoff/rag-course-platform.git
cd rag-course-platform
```

### 2. Запустить RAG сервис
```bash
cd rag-service

# Создать .env
cp .env.example .env
# Отредактировать: добавить YANDEX_API_KEY и YANDEX_FOLDER_ID

# Запустить через Docker
docker-compose up -d

# Проверить здоровье
curl http://localhost:8000/health
```

### 3. Индексировать материалы курса
```bash
# Индексация тестовых данных
python cli_indexer.py dir ../course-materials/test-data 1

# Индексация всех модулей
for i in {1..4}; do
  python cli_indexer.py dir ../course-materials/module-$i/lectures 1
done
```

### 4. Протестировать RAG
```bash
curl -X POST http://localhost:8000/ask \
  -H "Authorization: Bearer your-secret-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "course_id": 1,
    "question": "Что такое RAG?"
  }'
```

### 5. Установить Moodle плагин
```bash
# Скопировать в Moodle
cp -r moodle-plugin /path/to/moodle/blocks/aiassistant

# В Moodle: Site administration → Notifications
# Следовать инструкциям установки

# Настроить в: Site administration → Plugins → Blocks → AI Assistant
# - Service URL: http://localhost:8000
# - API Token: your-secret-token-here
```

## Production развертывание

### Требования к серверу
- Ubuntu 22.04 LTS
- 8 CPU / 16 GB RAM / 100 GB SSD
- Docker и Docker Compose
- Nginx

### Шаг 1: Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo apt install docker-compose-plugin
```

### Шаг 2: Деплой RAG сервиса
```bash
# Клонировать
git clone https://github.com/shuldeshoff/rag-course-platform.git
cd rag-course-platform/rag-service

# Настроить .env
nano .env
# Установить:
# - YANDEX_API_KEY
# - YANDEX_FOLDER_ID
# - API_TOKEN (сгенерировать надежный)
# - POSTGRES_PASSWORD

# Запустить
docker-compose up -d

# Проверить логи
docker-compose logs -f rag-service
```

### Шаг 3: Nginx конфигурация
```bash
sudo nano /etc/nginx/sites-available/rag-service

# Добавить:
server {
    listen 80;
    server_name rag.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 30s;
    }
}

# Активировать
sudo ln -s /etc/nginx/sites-available/rag-service /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# SSL
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d rag.yourdomain.com
```

### Шаг 4: Индексация материалов
```bash
cd rag-service

# Загрузить все лекции
python cli_indexer.py dir ../course-materials/module-1/lectures 1
python cli_indexer.py dir ../course-materials/module-2/lectures 1
python cli_indexer.py dir ../course-materials/module-3/lectures 1
python cli_indexer.py dir ../course-materials/module-4/lectures 1
python cli_indexer.py dir ../course-materials/module-5/lectures 1
python cli_indexer.py dir ../course-materials/module-6/lectures 1
python cli_indexer.py dir ../course-materials/module-7/lectures 1
python cli_indexer.py dir ../course-materials/module-8/lectures 1
```

## Мониторинг

### Проверка сервисов
```bash
# Статус Docker контейнеров
docker-compose ps

# Логи
docker-compose logs -f

# Health check
curl https://rag.yourdomain.com/health

# Статистика
curl https://rag.yourdomain.com/admin/stats/1 \
  -H "Authorization: Bearer $API_TOKEN"
```

### Метрики Prometheus
```bash
# Добавить в docker-compose.yml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

# prometheus.yml
scrape_configs:
  - job_name: 'rag-service'
    static_configs:
      - targets: ['rag-service:8000']
```

## Резервное копирование

### PostgreSQL
```bash
# Backup
docker exec rag-service-postgres-1 pg_dump -U postgres rag_service > backup.sql

# Restore
docker exec -i rag-service-postgres-1 psql -U postgres rag_service < backup.sql
```

### Qdrant
```bash
# Backup vectors
docker exec rag-service-qdrant-1 tar czf /tmp/qdrant-backup.tar.gz /qdrant/storage
docker cp rag-service-qdrant-1:/tmp/qdrant-backup.tar.gz ./

# Restore
docker cp ./qdrant-backup.tar.gz rag-service-qdrant-1:/tmp/
docker exec rag-service-qdrant-1 tar xzf /tmp/qdrant-backup.tar.gz -C /
```

## Troubleshooting

### RAG сервис не отвечает
```bash
# Проверить логи
docker-compose logs rag-service

# Перезапустить
docker-compose restart rag-service
```

### Ошибка подключения к Qdrant
```bash
# Проверить Qdrant
docker-compose logs qdrant
curl http://localhost:6333/collections

# Пересоздать коллекцию
python -c "from app.services.qdrant_service import qdrant_service; qdrant_service._ensure_collection()"
```

### YandexGPT ошибки
```bash
# Проверить API ключ
curl -X POST https://llm.api.cloud.yandex.net/foundationModels/v1/completion \
  -H "Authorization: Api-Key $YANDEX_API_KEY" \
  -d '{"modelUri":"gpt://..."}' 

# Проверить квоты в Yandex Cloud Console
```

### Медленные ответы
```bash
# Проверить Redis кэш
docker-compose logs redis
docker exec -it rag-service-redis-1 redis-cli PING

# Проверить размер эмбеддинг модели
docker-compose exec rag-service python -c "from app.services.embedder import embedder_service; print(embedder_service.dimension)"

# Увеличить ресурсы в docker-compose.yml
```

## Масштабирование

### Горизонтальное масштабирование
```yaml
# docker-compose.yml
services:
  rag-service:
    deploy:
      replicas: 3
    
  nginx:
    image: nginx
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
```

### Load Balancer (Nginx)
```nginx
upstream rag_backend {
    least_conn;
    server rag-service-1:8000;
    server rag-service-2:8000;
    server rag-service-3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://rag_backend;
    }
}
```

## Безопасность

### Рекомендации
- ✅ Использовать HTTPS
- ✅ Сильные API токены
- ✅ Регулярные обновления
- ✅ Firewall (UFW)
- ✅ Логирование доступа
- ✅ Rate limiting
- ✅ Регулярные бэкапы

### UFW настройка
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Поддержка

- GitHub Issues: https://github.com/shuldeshoff/rag-course-platform/issues
- Документация: /docs
- Email: support@example.com

