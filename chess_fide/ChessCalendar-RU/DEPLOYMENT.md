# Руководство по развертыванию Chess Calendar RU

## Быстрое развертывание (5 минут)

### Предварительные требования

- Docker и Docker Compose установлены
- Минимум 2GB RAM
- Минимум 5GB свободного места на диске

### Шаги

```bash
# 1. Клонирование репозитория
git clone <repository-url>
cd chess-calendar-ru

# 2. Настройка окружения
cp .env.example .env

# 3. Редактирование .env (обязательно!)
# Измените как минимум SECRET_KEY
nano .env  # или используйте любой редактор

# 4. Запуск
chmod +x start-all.sh  # Linux/Mac
./start-all.sh

# Для Windows:
start-all.bat

# 5. Создание администратора
docker-compose exec api-gateway python manage.py --action create-admin \
  --username admin \
  --email admin@example.com \
  --password SecurePassword123

# 6. Проверка
curl http://localhost:5000/health
```

## Production развертывание

### 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
```

### 2. Настройка .env для production

```bash
# Обязательные изменения
SECRET_KEY=<сгенерируйте случайный ключ>
FLASK_ENV=production
FLASK_DEBUG=False

# Рекомендуется PostgreSQL
DATABASE_URL=postgresql://user:password@postgres:5432/chess_calendar

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SESSION_COOKIE_SECURE=True
```

### 3. Настройка PostgreSQL (рекомендуется)

```yaml
# Добавьте в docker-compose.yml
postgres:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: chess_calendar
    POSTGRES_USER: chess_user
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  volumes:
    - postgres-data:/var/lib/postgresql/data
  networks:
    - chess-network
  restart: unless-stopped
```

### 4. SSL/TLS сертификаты

#### Вариант A: Let's Encrypt (бесплатно)

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Автоматическое обновление
sudo certbot renew --dry-run
```

#### Вариант B: Самоподписанный сертификат (для тестирования)

```bash
# Генерация сертификата
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx-selfsigned.key \
  -out nginx-selfsigned.crt

# Добавьте в nginx.conf
ssl_certificate /etc/nginx/ssl/nginx-selfsigned.crt;
ssl_certificate_key /etc/nginx/ssl/nginx-selfsigned.key;
```

### 5. Настройка Nginx

```nginx
# nginx-production.conf
upstream api_gateway {
    least_conn;
    server api-gateway:5000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;

    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # API Gateway
    location / {
        proxy_pass http://api_gateway;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;
}
```

### 6. Мониторинг и логирование

#### Prometheus + Grafana

```yaml
# Добавьте в docker-compose.yml
prometheus:
  image: prom/prometheus:latest
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
    - prometheus-data:/prometheus
  ports:
    - "9090:9090"
  networks:
    - chess-network

grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
  volumes:
    - grafana-data:/var/lib/grafana
  networks:
    - chess-network
  depends_on:
    - prometheus
```

#### ELK Stack (опционально)

```yaml
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
  environment:
    - discovery.type=single-node
  volumes:
    - elasticsearch-data:/usr/share/elasticsearch/data
  networks:
    - chess-network

logstash:
  image: docker.elastic.co/logstash/logstash:8.11.0
  volumes:
    - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
  networks:
    - chess-network
  depends_on:
    - elasticsearch

kibana:
  image: docker.elastic.co/kibana/kibana:8.11.0
  ports:
    - "5601:5601"
  networks:
    - chess-network
  depends_on:
    - elasticsearch
```

### 7. Резервное копирование

#### Автоматическое резервное копирование

```bash
# Создайте cron job
crontab -e

# Добавьте строку (ежедневно в 2:00)
0 2 * * * cd /path/to/chess-calendar-ru && docker-compose exec -T api-gateway python manage.py --action backup
```

#### Скрипт резервного копирования

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/chess-calendar"
DATE=$(date +%Y%m%d_%H%M%S)

# Создание директории
mkdir -p $BACKUP_DIR

# Резервное копирование базы данных
docker-compose exec -T postgres pg_dump -U chess_user chess_calendar > $BACKUP_DIR/db_$DATE.sql

# Резервное копирование Redis
docker-compose exec -T redis redis-cli SAVE
docker cp chess-calendar-ru_redis_1:/data/dump.rdb $BACKUP_DIR/redis_$DATE.rdb

# Сжатие
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz $BACKUP_DIR/db_$DATE.sql $BACKUP_DIR/redis_$DATE.rdb

# Удаление старых бэкапов (старше 30 дней)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +30 -delete

echo "Backup completed: backup_$DATE.tar.gz"
```

### 8. Масштабирование

#### Горизонтальное масштабирование

```bash
# Увеличение количества worker'ов
docker-compose up -d --scale celery-worker=4

# Запуск нескольких инстансов API Gateway
docker-compose up -d --scale api-gateway=3

# Настройка load balancer в nginx.conf
upstream api_gateway {
    least_conn;
    server api-gateway-1:5000;
    server api-gateway-2:5000;
    server api-gateway-3:5000;
}
```

#### Kubernetes (для больших нагрузок)

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: api-gateway
        image: chess-calendar/api-gateway:latest
        ports:
        - containerPort: 5000
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: chess-secrets
              key: secret-key
        - name: REDIS_URL
          value: redis://redis-service:6379/0
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 9. Мониторинг производительности

#### Настройка алертов

```yaml
# prometheus-alerts.yml
groups:
  - name: chess_calendar_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          
      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          
      - alert: CeleryQueueBacklog
        expr: celery_queue_length > 1000
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Celery queue backlog"
```

### 10. Безопасность

#### Firewall настройка

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Закрыть прямой доступ к сервисам
sudo ufw deny 5000:5009/tcp
sudo ufw deny 6379/tcp
```

#### Fail2Ban

```bash
# Установка
sudo apt install fail2ban

# Настройка для Nginx
sudo nano /etc/fail2ban/jail.local

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
maxretry = 5
bantime = 3600
```

### 11. Проверка развертывания

```bash
# Health checks
curl https://yourdomain.com/health

# Метрики
curl -H "Authorization: Bearer $ADMIN_TOKEN" https://yourdomain.com/metrics

# Flower
curl https://yourdomain.com:5555

# Проверка SSL
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

### 12. Troubleshooting

#### Проблемы с Docker

```bash
# Просмотр логов
docker-compose logs -f

# Перезапуск сервиса
docker-compose restart api-gateway

# Очистка неиспользуемых ресурсов
docker system prune -a
```

#### Проблемы с производительностью

```bash
# Проверка использования ресурсов
docker stats

# Проверка Redis
docker-compose exec redis redis-cli INFO

# Проверка Celery
docker-compose exec celery-worker celery -A app.celery_app inspect stats
```

## Чеклист развертывания

- [ ] Сервер подготовлен (Docker установлен)
- [ ] .env файл настроен (SECRET_KEY изменен)
- [ ] PostgreSQL настроен (для production)
- [ ] SSL сертификаты установлены
- [ ] Nginx настроен
- [ ] Firewall настроен
- [ ] Резервное копирование настроено
- [ ] Мониторинг настроен
- [ ] Health checks проходят
- [ ] Администратор создан
- [ ] Тестовые запросы успешны

## Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs`
2. Проверьте health checks
3. Обратитесь к [ARCHITECTURE.md](ARCHITECTURE.md)
4. Создайте issue в репозитории
