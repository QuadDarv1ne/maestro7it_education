# 📊 ELK Stack: Полное руководство по Elasticsearch, Logstash, Kibana и Beats

## 📋 Содержание

1. [Введение в ELK Stack](#введение-в-elk-stack)
2. [Архитектура ELK](#архитектура-elk)
3. [Elasticsearch](#elasticsearch)
4. [Logstash](#logstash)
5. [Kibana](#kibana)
6. [Beats](#beats)
7. [Установка и настройка](#установка-и-настройка)
8. [Практические примеры](#практические-примеры)
9. [Мониторинг и оптимизация](#мониторинг-и-оптимизация)

## Введение в ELK Stack

**ELK Stack** — это мощная платформа для управления логами и аналитики, состоящая из четырех основных компонентов:

- **E** - **Elasticsearch**: Распределенная поисковая и аналитическая система
- **L** - **Logstash**: Конвейер обработки данных
- **K** - **Kibana**: Инструмент визуализации и анализа
- **B** - **Beats**: Легковесные сборщики данных

### Основные применения:

- Централизованный сбор и анализ логов
- Мониторинг инфраструктуры
- Анализ безопасности (`SIEM`)
- Бизнес-аналитика
- Траблшутинг и дебаггинг

### Преимущества ELK Stack:

- **Масштабируемость**: Горизонтальное масштабирование
- **Производительность**: Быстрый поиск по большим объемам данных
- **Гибкость**: Поддержка различных источников данных
- **Визуализация**: Интерактивные дашборды
- **Открытый исходный код**: Бесплатное использование

---

## Архитектура ELK

### Общая архитектура данных:

```
[Источники данных] → [Beats] → [Logstash] → [Elasticsearch] → [Kibana]
                              ↓
                    [Elasticsearch напрямую]
```

### Компоненты потока данных:

1. **Beats** → Сбор данных с серверов
2. **Logstash** → Обработка и трансформация
3. **Elasticsearch** → Хранение и индексация
4. **Kibana** → Визуализация и анализ

### Типы данных:
- **Логи приложений** (Apache, Nginx, Tomcat)
- **Системные логи** (syslog, journalctl)
- **Метрики** (CPU, RAM, Disk I/O)
- **События безопасности** (firewall, IDS)
- **Бизнес-данные** (транзакции, события)

---

## Elasticsearch

### Описание
**Elasticsearch** — это распределенная поисковая и аналитическая система, построенная на Apache Lucene.

### Основные характеристики:
- **Документ-ориентированная NoSQL база данных**
- **RESTful API** для всех операций
- **Near Real-Time (NRT)** поиск
- **Горизонтальное масштабирование**
- **Высокая доступность** (репликация)

### Архитектура Elasticsearch:

```
Cluster (Кластер)
├── Node 1 (Master)
├── Node 2 (Data)
├── Node 3 (Data)
└── Node 4 (Coordinating)

Index (Индекс)
├── Shard 0 (Primary)
├── Shard 1 (Primary)
├── Shard 0 (Replica)
└── Shard 1 (Replica)
```

### Основные понятия:

#### Индекс (Index)
- Логическая группа документов
- Аналог таблицы в реляционной БД
- Может содержать миллиарды документов

#### Документ (Document)
- Основная единица хранения
- Формат JSON
- Пример:
```json
{
  "@timestamp": "2024-01-15T10:30:00Z",
  "message": "User login successful",
  "user_id": 12345,
  "ip_address": "192.168.1.100",
  "level": "INFO"
}
```

#### Шард (Shard)
- Физическое разделение индекса
- Primary shard - основная копия
- Replica shard - резервная копия

### Установка Elasticsearch:

```bash
# Ubuntu/Debian
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-8.x.list
sudo apt-get update
sudo apt-get install elasticsearch

# CentOS/RHEL
sudo rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
sudo yum install elasticsearch

# Запуск службы
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch
```

### Базовые операции:

#### Создание индекса:
```bash
curl -X PUT "localhost:9200/my_index" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "message": { "type": "text" },
      "level": { "type": "keyword" }
    }
  }
}'
```

#### Добавление документа:
```bash
curl -X POST "localhost:9200/my_index/_doc/1" -H 'Content-Type: application/json' -d'
{
  "timestamp": "2024-01-15T10:30:00Z",
  "message": "Application started successfully",
  "level": "INFO"
}'
```

#### Поиск документов:
```bash
# Простой поиск
curl -X GET "localhost:9200/my_index/_search?q=message:success"

# Поиск с DSL
curl -X GET "localhost:9200/my_index/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "message": "success"
    }
  },
  "sort": [
    { "timestamp": { "order": "desc" } }
  ],
  "size": 10
}'
```

### Настройка кластера:

```yaml
# /etc/elasticsearch/elasticsearch.yml
cluster.name: my-elk-cluster
node.name: node-1
network.host: 0.0.0.0
discovery.seed_hosts: ["192.168.1.10", "192.168.1.11", "192.168.1.12"]
cluster.initial_master_nodes: ["node-1", "node-2", "node-3"]
```

---

## Logstash

### Описание
**Logstash** — это серверная конвейерная система обработки данных с открытым исходным кодом.

### Архитектура Logstash:

```
Input Plugin → Filter Plugin → Output Plugin
     ↓              ↓              ↓
[Сбор данных]  [Обработка]    [Отправка]
```

### Основные этапы:
1. **Input**: Сбор данных из источников
2. **Filter**: Обработка и трансформация
3. **Output**: Отправка данных в назначение

### Установка Logstash:

```bash
# Ubuntu/Debian
sudo apt-get install logstash

# CentOS/RHEL
sudo yum install logstash

# Запуск службы
sudo systemctl enable logstash
sudo systemctl start logstash
```

### Пример конфигурации:

```ruby
# /etc/logstash/conf.d/syslog.conf

# Input - сбор системных логов
input {
  file {
    path => "/var/log/*.log"
    start_position => "beginning"
    sincedb_path => "/dev/null"
    ignore_older => 0
  }
  
  beats {
    port => 5044
  }
}

# Filter - обработка данных
filter {
  # Парсинг syslog
  if [type] == "syslog" {
    grok {
      match => { "message" => "%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:\\[%{POSINT:syslog_pid}\\])?: %{GREEDYDATA:syslog_message}" }
    }
    
    date {
      match => [ "syslog_timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
    }
  }
  
  # Обработка логов Apache
  if [type] == "apache" {
    grok {
      match => { "message" => "%{COMBINEDAPACHELOG}" }
    }
    
    geoip {
      source => "clientip"
    }
  }
  
  # Мутация полей
  mutate {
    remove_field => [ "@version" ]
    convert => { "bytes" => "integer" }
  }
}

# Output - отправка в Elasticsearch
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "logs-%{+YYYY.MM.dd}"
    user => "elastic"
    password => "your_password"
  }
  
  # Дополнительный вывод в файл для дебага
  stdout { codec => rubydebug }
}
```

### Популярные плагины:

#### Input Plugins:
- `file` - чтение из файлов
- `beats` - прием от Filebeat
- `syslog` - прием syslog сообщений
- `kafka` - чтение из Kafka
- `jdbc` - чтение из баз данных

#### Filter Plugins:
- `grok` - парсинг неструктурированных данных
- `mutate` - изменение полей
- `date` - парсинг дат
- `geoip` - геолокация IP
- `json` - парсинг JSON

#### Output Plugins:
- `elasticsearch` - отправка в ES
- `file` - запись в файл
- `kafka` - отправка в Kafka
- `email` - отправка email

### Тестирование конфигурации:

```bash
# Проверка синтаксиса
sudo -u logstash /usr/share/logstash/bin/logstash --config.test_and_exit -f /etc/logstash/conf.d/

# Тестовый запуск
sudo -u logstash /usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/test.conf
```

---

## Kibana

### Описание
**Kibana** — это инструмент визуализации и управления для Elasticsearch.

### Основные возможности:
- **Discover**: Исследование данных
- **Visualize**: Создание визуализаций
- **Dashboard**: Создание дашбордов
- **Dev Tools**: Консоль для запросов
- **Management**: Администрирование

### Установка Kibana:

```bash
# Ubuntu/Debian
sudo apt-get install kibana

# CentOS/RHEL
sudo yum install kibana

# Запуск службы
sudo systemctl enable kibana
sudo systemctl start kibana
```

### Базовая конфигурация:

```yaml
# /etc/kibana/kibana.yml
server.port: 5601
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://localhost:9200"]
elasticsearch.username: "kibana_system"
elasticsearch.password: "your_password"
kibana.index: ".kibana"
```

### Создание индекс паттерна:

1. Откройте Kibana: `http://localhost:5601`
2. Перейдите в **Stack Management** → **Index Patterns**
3. Создайте паттерн: `logs-*`
4. Выберите поле времени: `@timestamp`

### Примеры визуализаций:

#### 1. График логов по уровню важности:
```
Visualization Type: Vertical Bar
Metric: Count
Buckets: 
  - X-Axis: Terms(level.keyword)
  - Split Series: Date Histogram(@timestamp)
```

#### 2. Карта геолокации запросов:
```
Visualization Type: Coordinate Map
Metric: Unique Count(ip_address)
Geo Coordinates: geoip.location
```

#### 3. Таблица топ IP адресов:
```
Visualization Type: Data Table
Metric: Count
Buckets: Terms(clientip.keyword)
```

### Пример дашборда:

```json
{
  "title": "System Monitoring Dashboard",
  "panels": [
    {
      "id": "cpu-usage",
      "type": "visualization",
      "gridData": {"x": 0, "y": 0, "w": 24, "h": 15}
    },
    {
      "id": "memory-usage",
      "type": "visualization",
      "gridData": {"x": 24, "y": 0, "w": 24, "h": 15}
    },
    {
      "id": "error-logs",
      "type": "visualization",
      "gridData": {"x": 0, "y": 15, "w": 48, "h": 20}
    }
  ]
}
```

---

## Beats

### Описание
**Beats** — это легковесные сборщики данных, отправляющие данные напрямую в Elasticsearch или через Logstash.

### Основные типы Beats:

#### 1. Filebeat
Сбор лог-файлов

```yaml
# /etc/filebeat/filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/*.log
    - /var/log/apache2/*.log
    - /var/log/nginx/*.log
  fields:
    type: system
  fields_under_root: true

output.elasticsearch:
  hosts: ["localhost:9200"]
  username: "elastic"
  password: "your_password"

setup.kibana:
  host: "localhost:5601"
```

#### 2. Metricbeat
Сбор метрик системы

```yaml
# /etc/metricbeat/metricbeat.yml
metricbeat.modules:
- module: system
  metricsets:
    - cpu
    - memory
    - network
    - diskio
  enabled: true
  period: 10s

output.elasticsearch:
  hosts: ["localhost:9200"]
```

#### 3. Packetbeat
Анализ сетевого трафика

```yaml
# /etc/packetbeat/packetbeat.yml
packetbeat.interfaces:
  device: any

packetbeat.protocols:
- type: http
  ports: [80, 8080, 8000, 5000, 8002]

output.elasticsearch:
  hosts: ["localhost:9200"]
```

#### 4. Auditbeat
Аудит безопасности

```yaml
# /etc/auditbeat/auditbeat.yml
auditbeat.modules:
- module: auditd
  audit_rules: |
    -w /etc/passwd -p wa -k identity
    -w /etc/group -p wa -k identity

output.elasticsearch:
  hosts: ["localhost:9200"]
```

### Установка Filebeat:

```bash
# Ubuntu/Debian
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.11.3-amd64.deb
sudo dpkg -i filebeat-8.11.3-amd64.deb

# CentOS/RHEL
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.11.3-x86_64.rpm
sudo rpm -vi filebeat-8.11.3-x86_64.rpm

# Запуск
sudo systemctl enable filebeat
sudo systemctl start filebeat
```

---

## Установка и настройка

### Системные требования:

#### Минимальные:
- **RAM**: 4GB
- **CPU**: 2 cores
- **Disk**: 20GB свободного места
- **OS**: Linux 64-bit

#### Рекомендуемые:
- **RAM**: 16GB+
- **CPU**: 4+ cores
- **Disk**: SSD 100GB+
- **Network**: 1Gbps

### Пошаговая установка ELK Stack:

#### 1. Установка Java:
```bash
sudo apt update
sudo apt install openjdk-17-jdk
java -version
```

#### 2. Установка Elasticsearch:
```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt update
sudo apt install elasticsearch
```

#### 3. Установка Kibana:
```bash
sudo apt install kibana
```

#### 4. Установка Logstash:
```bash
sudo apt install logstash
```

#### 5. Установка Filebeat:
```bash
sudo apt install filebeat
```

### Конфигурация безопасности:

#### Включение SSL/TLS:
```yaml
# elasticsearch.yml
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.key: certs/elastic-certificates.key
xpack.security.transport.ssl.certificate: certs/elastic-certificates.crt
xpack.security.transport.ssl.certificate_authorities: certs/elastic-stack-ca.crt
```

#### Создание пользователей:
```bash
# Автоматическая настройка паролей
sudo /usr/share/elasticsearch/bin/elasticsearch-setup-passwords auto

# Ручная настройка
sudo /usr/share/elasticsearch/bin/elasticsearch-users useradd kibana_system -p your_password -r kibana_system
```

### Запуск служб:
```bash
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch logstash kibana filebeat
sudo systemctl start elasticsearch
sleep 30  # Ждем запуск Elasticsearch
sudo systemctl start logstash kibana filebeat
```

### Проверка установки:
```bash
# Проверка Elasticsearch
curl -X GET "localhost:9200/_cluster/health?pretty"

# Проверка Kibana
curl -I http://localhost:5601

# Проверка Logstash
sudo systemctl status logstash

# Проверка Filebeat
sudo filebeat test output
```

---

## Практические примеры

### Пример 1: Мониторинг веб-сервера

#### Конфигурация Filebeat для Nginx:
```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/nginx/access.log
    - /var/log/nginx/error.log
  fields:
    service: nginx
  multiline.pattern: '^[[:space:]]'
  multiline.negate: false
  multiline.match: after

processors:
- add_host_metadata: ~
- add_cloud_metadata: ~

output.logstash:
  hosts: ["localhost:5044"]
```

#### Logstash конфигурация для Nginx:
```ruby
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][service] == "nginx" {
    grok {
      match => { "message" => "%{IPORHOST:clientip} %{USER:ident} %{USER:auth} \\[%{HTTPDATE:timestamp}\\] \"(?:%{WORD:method} %{NOTSPACE:request}(?:%{URIPARAM:params})? %{NUMBER:version}|.*?)\" %{NUMBER:response} (?:%{NUMBER:bytes}|-) (?:(\"(?:%{URI:referrer}|-)\" \"(?:%{QS:agent}|-)\"|%{DATA}))" }
    }
    
    date {
      match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
    }
    
    geoip {
      source => "clientip"
    }
    
    useragent {
      source => "agent"
      target => "user_agent"
    }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "nginx-%{+YYYY.MM.dd}"
  }
}
```

#### Kibana дашборд для Nginx:
1. Создайте индекс паттерн: `nginx-*`
2. Создайте визуализации:
   - Response codes over time
   - Top URLs
   - Client IPs map
   - User agents pie chart
3. Соберите дашборд

### Пример 2: SIEM для безопасности

#### Auditbeat конфигурация:
```yaml
auditbeat.modules:
- module: auditd
  audit_rules: |
    # Monitor file access
    -w /etc/passwd -p wa -k identity
    -w /etc/shadow -p wa -k identity
    -w /etc/group -p wa -k identity
    
    # Monitor privileged commands
    -a always,exit -F arch=b64 -S execve -F euid=0 -k privileged
    
    # Monitor network connections
    -a always,exit -F arch=b64 -S connect -k network

- module: file_integrity
  paths:
    - /bin
    - /usr/bin
    - /sbin
    - /usr/sbin
    - /etc

output.elasticsearch:
  hosts: ["localhost:9200"]
  index: "auditbeat-%{[agent.version]}-%{+yyyy.MM.dd}"
```

### Пример 3: Мониторинг Docker контейнеров

#### Filebeat для Docker:
```yaml
filebeat.inputs:
- type: container
  paths: 
    - '/var/lib/docker/containers/*/*.log'
  stream: 'all'
  
processors:
- add_docker_metadata: ~
- decode_json_fields:
    fields: ["message"]
    target: "json"
    overwrite_keys: true

output.elasticsearch:
  hosts: ["localhost:9200"]
  indices:
    - index: "filebeat-docker-%{+yyyy.MM.dd}"
```

---

## Мониторинг и оптимизация

### Мониторинг кластера Elasticsearch:

#### Health Check:
```bash
curl -X GET "localhost:9200/_cluster/health?pretty"
```

#### Node Stats:
```bash
curl -X GET "localhost:9200/_nodes/stats?pretty"
```

#### Index Stats:
```bash
curl -X GET "localhost:9200/_stats?pretty"
```

### Оптимизация производительности:

#### Настройка JVM:
```bash
# /etc/elasticsearch/jvm.options
-Xms4g
-Xmx4g
-XX:+UseG1GC
-XX:G1ReservePercent=25
-XX:InitiatingHeapOccupancyPercent=30
```

#### Оптимизация индексов:
```bash
# Создание индекса с оптимальными настройками
curl -X PUT "localhost:9200/logs-optimized" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 5,
    "number_of_replicas": 1,
    "refresh_interval": "30s",
    "translog.durability": "async",
    "blocks": {
      "read_only_allow_delete": "false"
    }
  }
}'
```

#### ILM (Index Lifecycle Management):
```bash
# Создание политики ILM
curl -X PUT "localhost:9200/_ilm/policy/log-policy" -H 'Content-Type: application/json' -d'
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_age": "7d",
            "max_size": "50gb"
          }
        }
      },
      "delete": {
        "min_age": "30d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}'
```

### Резервное копирование:

#### Snapshot Repository:
```bash
# Создание репозитория для снапшотов
curl -X PUT "localhost:9200/_snapshot/my_backup" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/mnt/backups/elasticsearch"
  }
}'
```

#### Создание снапшота:
```bash
# Полный снапшот кластера
curl -X PUT "localhost:9200/_snapshot/my_backup/snapshot_1?wait_for_completion=true"

# Снапшот конкретного индекса
curl -X PUT "localhost:9200/_snapshot/my_backup/logs_snapshot?wait_for_completion=true" -H 'Content-Type: application/json' -d'
{
  "indices": "logs-*"
}'
```

### Troubleshooting:

#### Частые проблемы:

1. **Out of Memory**:
```bash
# Проверка использования памяти
curl -X GET "localhost:9200/_nodes/stats/jvm?pretty"
# Решение: увеличить heap size или добавить ноды
```

2. **Yellow/Red Cluster Status**:
```bash
# Проверка статуса
curl -X GET "localhost:9200/_cluster/allocation/explain?pretty"
# Решение: добавить реплики или ноды
```

3. **Slow Queries**:
```bash
# Профилирование запросов
curl -X GET "localhost:9200/_search?profile=true" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  }
}'
```

### Лучшие практики:

1. **Индексы**:
   - Используйте time-based индексы
   - Настройте ILM для автоматического управления
   - Не создавайте слишком много шардов

2. **Производительность**:
   - Мониторьте использование ресурсов
   - Используйте SSD для хранения
   - Настройте кэширование правильно

3. **Безопасность**:
   - Всегда используйте HTTPS
   - Настройте аутентификацию
   - Ограничьте доступ к API

---

## Заключение

ELK Stack представляет собой мощную платформу для лог-аналитики и мониторинга. Правильная настройка и использование всех компонентов позволяет эффективно:

- Собирать и хранить большие объемы данных
- Быстро искать по логам
- Создавать информативные визуализации
- Мониторить инфраструктуру в реальном времени

### Дальнейшее изучение:
- **Elasticsearch**: Advanced mapping, aggregations
- **Logstash**: Custom plugins, performance tuning
- **Kibana**: Advanced visualizations, alerting
- **Security**: X-Pack features, monitoring

### Полезные ресурсы:
- [Официальная документация](https://www.elastic.co/guide/index.html)
- [Elastic Community](https://discuss.elastic.co/)
- [GitHub репозитории](https://github.com/elastic)

Это руководство охватывает основы `ELK Stack`

Для продвинутого использования рекомендуется изучать официальную документацию и практические кейсы.

---

#### 💼 Автор: Дуплей Максим Игоревич

### 📲 Контакты:

- **Telegram №1:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)
- **Telegram №2:** [@dupley_maxim_1999](https://t.me/dupley_maxim_1999)

📅 **Дата:** 26.01.2026

▶️ Версия 1.0

---
> 📧 **Предложения по сотрудничеству:** maksimqwe42@mail.ru

---

### 💼 Профиль на Profi.ru
[![Profi.ru Profile](https://img.shields.io/badge/Profi.ru-Дуплей%20М.И.-FF6B35?style=for-the-badge)](https://profi.ru/profile/DupleyMI)

> Консультации и услуги программирования на платформе Profi.ru

---

### 📚 Услуги обучения
[![Обучение технологиям и языкам программирования на Kwork](https://img.shields.io/badge/Kwork-Обучение%20Программированию-blue?style=for-the-badge&logo=kwork)](https://kwork.ru/usability-testing/42465951/обучение-технологиям-и-языкам-программирования)

> Профессиональное обучение технологиям и языкам программирования. Персональные консультации и курсы от опытного преподавателя.

---

### 🏫 О школе
[![Website](https://img.shields.io/badge/Maestro7IT-school--maestro7it.ru-darkgreen?style=for-the-badge)](https://school-maestro7it.ru/)

> Инновационная школа программирования, специализирующаяся на подготовке специалистов в области современных технологий и языков программирования.