#!/bin/bash
# Automated backup script for Chess Calendar RU

set -e

BACKUP_DIR="backups/automated"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

echo "📦 Starting backup process..."

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
echo "Backing up database..."
if [ -f "instance/chess_calendar.db" ]; then
    cp instance/chess_calendar.db "$BACKUP_DIR/db_$DATE.db"
    echo "✅ Database backed up"
fi

# Backup Redis (if running)
if docker-compose ps redis | grep -q "Up"; then
    echo "Backing up Redis..."
    docker-compose exec -T redis redis-cli SAVE
    docker cp $(docker-compose ps -q redis):/data/dump.rdb "$BACKUP_DIR/redis_$DATE.rdb" 2>/dev/null || echo "⚠️  Redis backup skipped"
fi

# Backup .env file
if [ -f ".env" ]; then
    cp .env "$BACKUP_DIR/env_$DATE.backup"
    echo "✅ Environment file backed up"
fi

# Compress backups
echo "Compressing backups..."
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" -C "$BACKUP_DIR" \
    $(ls "$BACKUP_DIR" | grep "_$DATE\." | grep -v ".tar.gz") 2>/dev/null || true

# Remove uncompressed files
rm -f "$BACKUP_DIR"/*_$DATE.{db,rdb,backup} 2>/dev/null || true

# Clean old backups
echo "Cleaning old backups (older than $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete

# Show backup info
BACKUP_SIZE=$(du -h "$BACKUP_DIR/backup_$DATE.tar.gz" | cut -f1)
echo ""
echo "✅ Backup completed!"
echo "📁 Location: $BACKUP_DIR/backup_$DATE.tar.gz"
echo "📊 Size: $BACKUP_SIZE"
echo "🗑️  Backups older than $RETENTION_DAYS days have been removed"
