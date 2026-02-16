#!/bin/bash
# Production deployment script for Chess Calendar RU

set -e

echo "🚀 Starting production deployment..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="backups/pre-deployment"
LOG_FILE="logs/deployment-$(date +%Y%m%d_%H%M%S).log"

# Functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

# Pre-deployment checks
log "Running pre-deployment checks..."

# Check if .env exists
if [ ! -f .env ]; then
    error ".env file not found! Please create it from .env.example"
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    error "Docker is not running. Please start Docker and try again."
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    error "docker-compose is not installed. Please install it and try again."
fi

# Backup current database
log "Creating backup..."
mkdir -p "$BACKUP_DIR"
if [ -f "instance/chess_calendar.db" ]; then
    cp instance/chess_calendar.db "$BACKUP_DIR/chess_calendar-$(date +%Y%m%d_%H%M%S).db"
    log "Database backup created"
fi

# Pull latest changes (if using git)
if [ -d .git ]; then
    log "Pulling latest changes from git..."
    git pull origin main || warning "Git pull failed or not configured"
fi

# Build Docker images
log "Building Docker images..."
docker-compose build --no-cache || error "Docker build failed"

# Stop existing containers
log "Stopping existing containers..."
docker-compose down

# Start services
log "Starting services..."
docker-compose up -d || error "Failed to start services"

# Wait for services to be healthy
log "Waiting for services to be healthy..."
sleep 15

# Health checks
log "Running health checks..."
services=("api-gateway:5000" "tournament-service:5001" "user-service:5002")
failed_services=()

for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if curl -f -s "http://localhost:$port/health" > /dev/null; then
        log "✅ $name is healthy"
    else
        warning "❌ $name health check failed"
        failed_services+=("$name")
    fi
done

# Database migrations (if needed)
log "Running database migrations..."
docker-compose exec -T api-gateway python manage.py migrate || warning "Migration failed or not configured"

# Clear cache
log "Clearing cache..."
docker-compose exec -T redis redis-cli FLUSHDB || warning "Cache clear failed"

# Restart Celery workers to pick up new code
log "Restarting Celery workers..."
docker-compose restart celery-worker celery-beat

# Final status
echo ""
log "========================================="
if [ ${#failed_services[@]} -eq 0 ]; then
    log "✅ Deployment completed successfully!"
else
    warning "⚠️  Deployment completed with warnings"
    warning "Failed services: ${failed_services[*]}"
fi
log "========================================="

# Show running services
log "Running services:"
docker-compose ps

# Show logs
log "Recent logs:"
docker-compose logs --tail=50

echo ""
log "📍 Access points:"
log "   - API Gateway: http://localhost:5000"
log "   - Flower: http://localhost:5555"
log "   - Health check: curl http://localhost:5000/health"
echo ""
log "📝 Deployment log saved to: $LOG_FILE"
log "💾 Backup saved to: $BACKUP_DIR"
