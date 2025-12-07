#!/bin/bash

# Deployment script for RAG Course Platform on sul-lnx
# Usage: ./deploy.sh

set -e

echo "==================================="
echo "RAG Course Platform Deployment"
echo "==================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}Please do not run as root${NC}"
    exit 1
fi

# Variables
DEPLOY_DIR="/opt/rag-course-platform"
DOMAIN="ragcourse.ru"

echo ""
echo "Step 1: Preparing deployment directory..."
sudo mkdir -p $DEPLOY_DIR
sudo chown $USER:$USER $DEPLOY_DIR
cd $DEPLOY_DIR

echo ""
echo "Step 2: Cloning repository..."
if [ -d ".git" ]; then
    echo "Repository already exists, pulling latest changes..."
    git pull origin main
else
    git clone https://github.com/shuldeshoff/rag-course-platform.git .
fi

echo ""
echo "Step 3: Setting up environment..."
cd deployment
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env file and set your credentials:${NC}"
    echo "  - YANDEX_API_KEY"
    echo "  - YANDEX_FOLDER_ID"
    echo "  - RAG_API_TOKEN (generate strong token)"
    echo "  - Database passwords"
    echo ""
    read -p "Press enter when .env is configured..."
else
    echo ".env already exists, skipping..."
fi

echo ""
echo "Step 4: Building Docker images..."
docker-compose build

echo ""
echo "Step 5: Starting services..."
docker-compose up -d

echo ""
echo "Step 6: Waiting for services to be ready..."
sleep 30

# Check services health
echo "Checking PostgreSQL..."
docker-compose exec -T postgres pg_isready -U postgres || echo -e "${YELLOW}PostgreSQL not ready yet${NC}"

echo "Checking Qdrant..."
curl -sf http://localhost:6333/readiness > /dev/null && echo -e "${GREEN}Qdrant is ready${NC}" || echo -e "${YELLOW}Qdrant not ready yet${NC}"

echo "Checking Redis..."
docker-compose exec -T redis redis-cli ping > /dev/null && echo -e "${GREEN}Redis is ready${NC}" || echo -e "${YELLOW}Redis not ready yet${NC}"

echo ""
echo "Step 7: Configuring Nginx..."
sudo cp nginx-ragcourse.conf /etc/nginx/sites-available/ragcourse.ru

if [ ! -L /etc/nginx/sites-enabled/ragcourse.ru ]; then
    sudo ln -s /etc/nginx/sites-available/ragcourse.ru /etc/nginx/sites-enabled/
    echo "Nginx config enabled"
fi

# Test nginx config
sudo nginx -t

echo ""
echo "Step 8: Setting up SSL with Let's Encrypt..."
read -p "Do you want to setup SSL now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN
    sudo systemctl reload nginx
else
    echo -e "${YELLOW}Skipping SSL setup. Run manually: sudo certbot --nginx -d $DOMAIN${NC}"
    echo "For now, reload nginx without SSL:"
    sudo systemctl reload nginx
fi

echo ""
echo "Step 9: Indexing course materials..."
cd $DEPLOY_DIR
read -p "Do you want to index course materials now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose exec rag-service python cli_indexer.py dir /app/../course-materials/test-data 1
    
    for i in {1..8}; do
        echo "Indexing module $i..."
        docker-compose exec rag-service python cli_indexer.py dir /app/../course-materials/module-$i/lectures 1 || true
    done
    echo -e "${GREEN}Course materials indexed${NC}"
else
    echo -e "${YELLOW}Skipping indexing. Run manually later.${NC}"
fi

echo ""
echo "==================================="
echo -e "${GREEN}Deployment completed!${NC}"
echo "==================================="
echo ""
echo "Services status:"
docker-compose ps
echo ""
echo "Access points:"
echo "  - Moodle: https://$DOMAIN"
echo "  - RAG API: https://$DOMAIN/rag/"
echo "  - API Docs: https://$DOMAIN/rag/docs"
echo ""
echo "Moodle admin credentials:"
echo "  Username: admin"
echo "  Password: (check .env file)"
echo ""
echo "Next steps:"
echo "  1. Access Moodle and complete setup"
echo "  2. Install AI Assistant block plugin"
echo "  3. Configure plugin: Site admin → Plugins → Blocks → AI Assistant"
echo "     - Service URL: https://$DOMAIN/rag"
echo "     - API Token: (from .env file)"
echo ""
echo "Logs:"
echo "  docker-compose logs -f [service_name]"
echo ""
echo "To restart services:"
echo "  cd $DEPLOY_DIR/deployment && docker-compose restart"
echo ""

