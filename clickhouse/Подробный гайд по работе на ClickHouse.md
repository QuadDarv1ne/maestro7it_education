# ClickHouse — установка, настройка и работа (подробное руководство)

**Автор: Дуплей Максим Игоревич**  
**ORCID:** https://orcid.org/0009-0007-7605-539X  
**GitHub:** https://github.com/QuadDarv1ne/

> **Язык документа:** русский

---

## Оглавление

1. Введение
2. Требования и подготовка окружения
3. Установка
  - Ubuntu / Debian (APT)
  - CentOS / RHEL (YUM)
  - Docker
  - macOS (brew)
  - Windows (Docker)
4. Быстрая проверка работоспособности
5. Основные конфигурационные файлы
6. Запуск и управление сервисом
7. Базовая работа: clickhouse-client и примеры
8. Загрузка SQL-скрипта (пример вашей обучающей БД)
9. Настройка хранения и производительности
10. Репликация и распределённые таблицы (кластер)
11. Резервное копирование и восстановление
12. Мониторинг и алертинг (Prometheus + Grafana)
13. Безопасность и доступы
14. Практические советы и отладка
15. Полезные команды и FAQ
16. Ресурсы и ссылки

---

## 1. Введение

`ClickHouse` — колоночная СУБД для аналитики в реальном времени.

Документ описывает шаги по установке, базовой настройке, рекомендации по производительности и примеры работы с учебной базой данных.

## 2. Требования и подготовка окружения

- Linux-сервер (рекомендуется Ubuntu LTS / CentOS) или Docker.
- Не менее 2 CPU, 4–8 GB RAM для тестов; для производственных нагрузок — больше.
- **Диск:** NVMe/SATA — для OLAP нагрузки лучше быстрый диск; ClickHouse активно использует I/O.
- Установите `curl`, `wget`, `tar`, `systemd`

## 3. Установка

### 3.1 Ubuntu / Debian (APT)

```bash
# Добавить репозиторий
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E0C56BD4
sudo apt-get install apt-transport-https ca-certificates -y
echo "deb https://repo.clickhouse.com/deb/stable/ main/" | sudo tee /etc/apt/sources.list.d/clickhouse.list
sudo apt update
sudo apt install -y clickhouse-server clickhouse-client
```
После установки сервисы находятся под systemd: `clickhouse-server`.

### 3.2 CentOS / RHEL (YUM)

```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://repo.clickhouse.com/rpm/stable/x86_64
sudo yum install -y clickhouse-server clickhouse-client
```

### 3.3 Docker (рекомендуется для локальной разработки)

```bash
docker run -d --name clickhouse-server --ulimit nofile=262144:262144 -p 9000:9000 -p 8123:8123 -p 9009:9009 yandex/clickhouse-server:latest
```
Для постоянного использования монтируйте томы данных и конфигурации.

### 3.4 macOS (Homebrew)

```bash
brew install clickhouse
# или запустить контейнер Docker, как выше
```

### 3.5 Windows

Официальный пакет под Windows отсутствует — используйте Docker контейнер.

## 4. Быстрая проверка работоспособности

**После установки:**

```bash
sudo systemctl start clickhouse-server
sudo systemctl enable clickhouse-server
clickhouse-client --query="SELECT version()"
```

Если используется Docker, подключитесь к контейнеру: `docker exec -it clickhouse-server clickhouse-client`

## 5. Основные конфигурационные файлы

**Расположение по умолчанию:** `/etc/clickhouse-server/`

- `config.xml` — основная конфигурация сервера (сеть, порты, логирование).
- `users.xml` и `users.d/*` — пользователи, пароли, права и профили.
- `metrika.xml`, `keeper.xml` — при использовании ClickHouse Keeper / Zookeeper.

**Совет:** не правьте `config.xml` вручную на проде без бэкапа. Используйте `users.d/` для добавления пользователей.

## 6. Запуск и управление сервисом

```bash
# systemd
sudo systemctl start clickhouse-server
sudo systemctl stop clickhouse-server
sudo systemctl status clickhouse-server
# Просмотр логов
sudo journalctl -u clickhouse-server -f
```

## 7. Базовая работа: clickhouse-client и примеры

- **Подключение (TCP):** `clickhouse-client --host 127.0.0.1 --port 9000`
- **HTTP-интерфейс:** `curl 'http://localhost:8123/?query=SELECT+1'`
- **Выполнение SQL-файла:** `clickhouse-client --multiquery < myscript.sql`

**Пример создания базы и таблицы:**

```sql
CREATE DATABASE IF NOT EXISTS training;
CREATE TABLE training.test (id UInt64, ts DateTime, v Float32) ENGINE = MergeTree() PARTITION BY toYYYYMM(ts) ORDER BY (id);
```

## 8. Загрузка SQL-скрипта (пример вашей обучающей БД)

**Если вы сохранили `clickhouse_training_db.sql` в текущей директории на сервере:**

```bash
clickhouse-client --multiquery < clickhouse_training_db.sql
```

Если файл большой — убедитесь, что `ulimit -n` и `ulimit -u` достаточно велики, и что в `users.xml` профиль позволяет длинные запросы.

## 9. Настройка хранения и производительности

- Таблицы MergeTree: **PARTITION BY** и **ORDER BY** — ключ к производительности.
- `index_granularity` подбирается эмпирически (стандарт 8192).
- Используйте `LowCardinality` для часто дублирующихся строк.
- Сжимающие CODEC: `CODEC(ZSTD(3))` для полей `String`.
- TTL для автоматического удаления старых данных: `TTL ts + INTERVAL 365 DAY DELETE`.
- Для OLAP нагрузок используйте быстрые диски и достаточный объём RAM.

## 10. Репликация и распределённые таблицы (кластер)

- Для репликации необходим Zookeeper или ClickHouse Keeper (замена ZK).
- Используйте `ReplicatedMergeTree` для реплицируемых партиций.

- **Пример создания реплицируемой таблицы:**

```sql
CREATE TABLE db.table ON CLUSTER '{cluster}' (
  ...
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/table','{replica}')
PARTITION BY toYYYYMM(ts) ORDER BY (id);
```

- Для распределённых запросов используйте `Distributed` таблицы, которые направляют запросы по шардам.

## 11. Резервное копирование и восстановление

- Инструмент `clickhouse-backup` (сообщество) — удобен для S3/локальных бэкапов.
- Native backup: `BACKUP TABLE ... TO DISK` (в новых версиях) или копирование директорий данных при остановленном сервисе.
- Регулярно проверяйте restore-процедуры на тестовом окружении.

## 12. Мониторинг и алертинг (Prometheus + Grafana)

- ClickHouse экспортирует метрики в Prometheus (включить в `config.xml`).
- Используйте готовые дашборды Grafana (Official ClickHouse dashboards).
- Следите за метриками: MergeTree merges, memory usage, query_latency, queue_size.

## 13. Безопасность и доступы

- Изолируйте порт 9000 (TCP) и 8123 (HTTP) через firewall.
- Используйте TLS для HTTP и inter-server соединений.
- Создавайте пользователей с ограниченными правами в `users.d/`.
- Используйте RBAC и роли (начиная с соответствующих версий ClickHouse).

## 14. Практические советы и отладка

- `system.query_log`, `system.mutations`, `system.replication_queue` — первичные места для диагностики.
- Для медленных запросов используйте `EXPLAIN` и `trace/log`.
- Если много мелких файлов — настройте `merge_with_recompression`, `parts_to_throw_insert`.
- Для больших INSERT используйте `INSERT INTO ... FORMAT CSV` или batched inserts.

## 15. Полезные команды и FAQ

- Просмотреть базы: `SHOW DATABASES`.
- Просмотреть таблицы: `SHOW TABLES IN training`.
- Информация о таблице: `SELECT * FROM system.tables WHERE database='training' AND name='messages'`.

## 16. Ресурсы и ссылки

- **Официальная документация:** https://clickhouse.com/docs
- **Репозиторий:** https://github.com/ClickHouse/ClickHouse
- **ClickHouse Backup:** https://github.com/AlexAkulov/clickhouse-backup

---

**Если хотите, я могу:**

- экспортировать этот `.md` файл и дать ссылку на скачивание;
- дополнить секцию для конкретной ОС / окружения;
- сделать пошаговый скрипт для создания кластера из трёх нод.

---

*Документ сгенерирован автоматически. При необходимости дополню разделы или добавлю примеры команд под вашу инфраструктуру.*
