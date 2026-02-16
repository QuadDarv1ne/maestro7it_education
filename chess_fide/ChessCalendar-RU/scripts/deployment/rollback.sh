#!/bin/bash
# Rollback script for Chess Calendar RU

set -e

echo "🔄 Starting rollback..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BACKUP_DIR="backups/pre-deployment"

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Find latest backup
LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/chess_calendar-*.db 2>/dev/null | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    error "No backup found in $BACKUP_DIR"
fi

log "Found backup: $LATEST_BACKUP"
read -p "Do you want to restore from this backup? (y/n) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log "Rollback cancelled"
    exit 0
fi

# Stop services
log "Stopping services..."
docker-compose down

# Restore database
log "Restoring database..."
mkdir -p instance
cp "$LATEST_BACKUP" instance/chess_calendar.db

# Start services
log "Starting services..."
docker-compose up -d

# Wait and check health
sleep 10
log "Checking health..."
curl -f http://localhost:5000/health || error "Health check failed"

log "✅ Rollback completed successfully!"
