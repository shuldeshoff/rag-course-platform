# RAG Course Platform - Deployment on sul-lnx

## Prerequisites
- Ubuntu 24.04 LTS ✅
- Docker & Docker Compose ✅
- Domain: ragcourse.ru (DNS configured)
- 8+ GB RAM available ✅
- Ports available: 8000, 8080

## Quick Deploy

### 1. Upload files to server
```bash
# From local machine
cd /Users/sul/CursorProjects/Moodle
rsync -avz --exclude '.git' deployment/ sul-lnx:/tmp/rag-deployment/
```

### 2. Run deployment script
```bash
# On sul-lnx
ssh sul-lnx
cd /tmp/rag-deployment
chmod +x deploy.sh
./deploy.sh
```

## Manual Deploy Steps

### 1. Prepare directories
```bash
sudo mkdir -p /opt/rag-course-platform
sudo chown $USER:$USER /opt/rag-course-platform
cd /opt/rag-course-platform
```

### 2. Clone repository
```bash
git clone https://github.com/shuldeshoff/rag-course-platform.git .
cd deployment
```

### 3. Configure environment
```bash
cp .env.example .env
nano .env

# Set values:
# - YANDEX_API_KEY
# - YANDEX_FOLDER_ID
# - RAG_API_TOKEN (generate: openssl rand -hex 32)
# - Strong passwords for databases
```

### 4. Start services
```bash
docker-compose up -d
```

### 5. Check services
```bash
docker-compose ps
docker-compose logs -f

# Check health
curl http://localhost:8000/health
curl http://localhost:8080
```

### 6. Configure Nginx
```bash
sudo cp nginx-ragcourse.conf /etc/nginx/sites-available/ragcourse.ru
sudo ln -s /etc/nginx/sites-available/ragcourse.ru /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. Setup SSL
```bash
sudo certbot --nginx -d ragcourse.ru -d www.ragcourse.ru
```

### 8. Index course materials
```bash
cd /opt/rag-course-platform
docker-compose exec rag-service python cli_indexer.py dir ../course-materials/test-data 1

# Index all modules
for i in {1..8}; do
  docker-compose exec rag-service python cli_indexer.py dir ../course-materials/module-$i/lectures 1
done
```

## Install Moodle Plugin

### 1. Copy plugin to Moodle container
```bash
cd /opt/rag-course-platform
docker cp moodle-plugin moodle:/opt/bitnami/moodle/blocks/aiassistant
docker-compose exec moodle chown -R daemon:daemon /opt/bitnami/moodle/blocks/aiassistant
```

### 2. Install via Moodle UI
- Login to Moodle as admin
- Go to: Site administration → Notifications
- Follow installation wizard

### 3. Configure plugin
- Site administration → Plugins → Blocks → AI Assistant
- Set:
  - Service URL: `https://ragcourse.ru/rag`
  - API Token: (from .env)
  - Timeout: 10 seconds
  - Enable logging: Yes

### 4. Add block to course
- Open any course
- Turn editing on
- Add block → AI Assistant

## URLs

- **Moodle:** https://ragcourse.ru
- **RAG API:** https://ragcourse.ru/rag/
- **API Docs:** https://ragcourse.ru/rag/docs
- **Health:** https://ragcourse.ru/rag/health

## Monitoring

```bash
# Services status
docker-compose ps

# Logs
docker-compose logs -f rag-service
docker-compose logs -f moodle

# Resources
docker stats

# RAG service health
curl https://ragcourse.ru/rag/health

# Database connections
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
```

## Backup

### PostgreSQL
```bash
# Backup both databases
docker-compose exec postgres pg_dumpall -U postgres > backup_$(date +%Y%m%d).sql

# Restore
cat backup_20241207.sql | docker-compose exec -T postgres psql -U postgres
```

### Qdrant vectors
```bash
# Backup
docker-compose exec qdrant tar czf /tmp/qdrant-backup.tar.gz /qdrant/storage
docker cp qdrant:/tmp/qdrant-backup.tar.gz ./qdrant-backup_$(date +%Y%m%d).tar.gz

# Restore
docker cp qdrant-backup_20241207.tar.gz qdrant:/tmp/
docker-compose exec qdrant tar xzf /tmp/qdrant-backup.tar.gz -C /
docker-compose restart qdrant
```

### Moodle data
```bash
# Backup moodledata
docker run --rm -v deployment_moodledata:/data -v $(pwd):/backup alpine \
  tar czf /backup/moodledata_$(date +%Y%m%d).tar.gz -C /data .
```

## Troubleshooting

### Moodle not accessible
```bash
docker-compose logs moodle
docker-compose restart moodle
```

### RAG service errors
```bash
docker-compose logs rag-service
# Check YandexGPT API key
docker-compose exec rag-service env | grep YANDEX
```

### Database connection issues
```bash
docker-compose exec postgres psql -U postgres -l
docker-compose restart postgres
```

### Clear Redis cache
```bash
docker-compose exec redis redis-cli FLUSHALL
```

## Updates

```bash
cd /opt/rag-course-platform
git pull origin main
docker-compose down
docker-compose build
docker-compose up -d
```

## Maintenance

### Restart all services
```bash
cd /opt/rag-course-platform/deployment
docker-compose restart
```

### Stop services
```bash
docker-compose stop
```

### Remove everything (DANGER)
```bash
docker-compose down -v
sudo rm -rf /opt/rag-course-platform
```

