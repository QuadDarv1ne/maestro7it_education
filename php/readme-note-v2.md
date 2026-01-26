# Руководство по работе с Symfony, Composer и Laragon

## Основные команды Composer

### Обновление пакетов
```bash
composer update "symfony/*" --with-all-dependencies
```

### Обновление Composer (если старая версия):
```bash
composer self-update
```
или
```bash
composer self-update --stable
```

### Проверка OpenSSL - Убедитесь, что проблема с openssl решена:
```bash
php -m | grep openssl
```

## Для разных типов проектов

### Для API (API Platform):
```bash
composer require api
```

### Для консольного приложения:
```bash
composer require symfony/console
```

### Для веб-проекта (Symfony):
```bash
composer require symfony/symfony
composer require symfony/webapp-pack
```

## Laravel

1. Проверить установку PHP
2. Проверить установку Laragon или Open Server
3. Проверить установку Composer

---

## 🚀 Полный мануал по работе с Symfony, Composer и Laragon

### 📦 1. Настройка локального окружения

#### Проверка и установка базовых компонентов

| Компонент | Команда проверки | Установка/обновление |
|-----------|------------------|----------------------|
| PHP | php -v | В Laragon: Tools → Runtime |
| Composer | composer --version | composer self-update --stable |
| OpenSSL | php -m \| grep openssl | sudo apt install openssl php-openssl (Linux) |

### 🖥️ Laragon специфика

- Автоматический хостинг: Проекты доступны по ваш-проект.test
- Переключение PHP: PHP → Version в меню Laragon
- Терминал: Всегда используйте Laragon Terminal для правильного PATH

### 🔄 2. Работа с Composer

#### Основные команды

```bash
# Инициализация проекта
composer init

# Установка зависимостей из composer.json
composer install

# Добавление пакета
composer require имя-пакета

# Обновление всех пакетов
composer update

# Обновление конкретных пакетов
composer update "symfony/*" --with-all-dependencies

# Автозагрузка классов
composer dump-autoload
```

### 🏗️ Создание проектов

| Тип проекта | Команда |
|-------------|---------|
| Symfony (веб) | composer create-project symfony/skeleton:"6.4.*" my-project |
| Symfony (веб с фронтендом) | composer create-project symfony/website-skeleton:"6.4.*" my-project |
| Laravel | composer create-project laravel/laravel my-project |
| API Platform | composer create-project api/api-platform my-project |

### 🎯 3. Работа с Symfony

#### Установка компонентов

```bash
# Базовый Symfony
composer require symfony/symfony

# Полный веб-пакет (рекомендуется для начала)
composer require symfony/webapp-pack

# Консольные приложения
composer require symfony/console

# API проект
composer require api

# Инструменты разработки
composer require --dev symfony/maker-bundle
composer require --dev symfony/debug-bundle
composer require --dev symfony/profiler-pack
```

### 📁 Базовая структура Symfony проекта

```
ваш-проект/
├─ public/           # Корневая веб-директория (index.php)
├─ src/              # Исходный код приложения
├─ config/           # Конфигурации (routes, services)
├─ templates/        # Шаблоны Twig
├─ var/              # Кеш, логи, скомпилированные файлы
├─ vendor/           # Зависимости Composer
└─ .env              # Переменные окружения
```

### ⬆️ 4. Обновление версий

#### 🔄 Обновление Symfony

```bash
# 1. Проверьте текущую версию
php bin/console about | grep Symfony

# 2. Обновитесь до последней минорной версии текущего мажора
# В composer.json измените "symfony/*": "6.1.*" → "symfony/*": "6.4.*"
composer update "symfony/*" --with-all-dependencies

# 3. Исправьте все deprecation warnings в dev-режиме

# 4. Для мажорного обновления (6.4 → 7.0):
# - Обновите extra.symfony.require в composer.json
# - Убедитесь в совместимости PHP (Symfony 7.x требует PHP 8.2+)
composer update "symfony/*" --with-all-dependencies
```

#### 📊 Таблица совместимости Symfony

| Symfony | Требует PHP | LTS | Статус |
|---------|-------------|-----|--------|
| 8.x | >= 8.4 | Нет | Актуальная |
| 7.4 | >= 8.2 | Да | LTS (рекомендуется) |
| 6.4 | >= 8.1 | Да | LTS (стабильная) |
| 5.4 | >= 7.2 | Да | Старая LTS |

#### ⬆️ Обновление PHP в Laragon

1. Tools → Runtime
2. Выберите нужную версию PHP → +Install
3. PHP → Version → Выберите установленную версию
4. Перезапустите Laragon: Restart

### 🛠️ 5. Решение частых проблем

#### ❌ "The openssl extension is required"

```bash
# Проверка
php -m | grep openssl

# Решение для Windows (Laragon):
# 1. В php.ini раскомментируйте: extension=openssl
# 2. Перезапустите Laragon

# Временное отключение TLS (не для production!):
composer config -g disable-tls true
```

#### ❌ Ошибки при обновлении Symfony

```bash
# 1. Создайте backup
git commit -am "Before Symfony update"

# 2. Обновите до последней минорной версии текущего мажора
composer update "symfony/*" --with-all-dependencies

# 3. Если есть конфликты:
# - Обновляйте пакеты по одному
# - Проверьте совместимость сторонних бандлов

# 4. Очистите кеш после обновления
rm -rf var/cache/*
# Для Windows:
rmdir /s /q var\\cache\\*
```

#### ❌ Ошибки автозагрузки

```bash
# Перегенерируйте автозагрузку
composer dump-autoload

# Оптимизируйте для production
composer dump-autoload --optimize
```

### 📝 6. Пример composer.json для Symfony 7.4

```json
{
    "name": "vendor/project-name",
    "type": "project",
    "license": "MIT",
    "require": {
        "php": ">=8.2",
        "symfony/symfony": "^7.4",
        "symfony/runtime": "^7.4"
    },
    "require-dev": {
        "symfony/debug-bundle": "^7.4",
        "symfony/maker-bundle": "^1.50"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    },
    "scripts": {
        "auto-scripts": {
            "cache:clear": "symfony-cmd",
            "assets:install": "symfony-cmd"
        }
    },
    "extra": {
        "symfony": {
            "allow-contrib": false,
            "require": "7.4.*"
        }
    }
}
```

### 💡 7. Полезные советы

#### 🚀 Быстрый старт нового проекта

```bash
# 1. Установите нужную версию PHP в Laragon
# 2. Создайте проект
composer create-project symfony/website-skeleton:"7.4.*" my-project
# 3. Перейдите в директорию
cd my-project
# 4. Запустите веб-сервер
symfony server:start
```

#### 🔍 Проверка окружения

```bash
# Полная проверка готовности к Symfony
php bin/console about

# Проверка конфигурации PHP
php --ini

# Проверка расширений PHP (должны быть: openssl, mbstring, xml, ctype, iconv)
php -m
```

#### ⚡ Производительность

```bash
# Включение кеша OPcache (добавьте в php.ini)
opcache.enable=1
opcache.memory_consumption=256

# Оптимизация Composer для production
composer install --no-dev --optimize-autoloader
```

### ✅ Чек-лист нового проекта

- [ ] Установлен Laragon с нужной версией PHP (≥8.2 для Symfony 7.4)
- [ ] Composer обновлён до последней версии
- [ ] OpenSSL расширение активно
- [ ] Создан composer.json с корректными зависимостями
- [ ] Установлены зависимости: composer install
- [ ] Настроен .env файл (база данных, секреты)
- [ ] Проект открывается по http://my-project.test
- [ ] Панель отладки Symfony доступна в dev-режиме

### 📚 Полезные ресурсы

- Официальная документация Symfony: https://symfony.com/doc/current/
- Composer документация: https://getcomposer.org/doc/
- PHP.NET для загрузки PHP: https://www.php.net/downloads.php
- Laragon документация: https://laragon.org/docs/

---

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram №1:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)

📲 **Telegram №2:** [@dupley_maxim_1999](https://t.me/dupley_maxim_1999)

📅 **Дата:** 26.01.2026

▶️ **Версия 1.0**

```textline
※ Предложения по сотрудничеству можете присылать на почту ※
📧 maksimqwe42@mail.ru
```

---

### 💼 Профиль на Profi.ru

[![Profi.ru Profile](https://img.shields.io/badge/Profi.ru-Дуплей%20М.И.-FF6B35?style=for-the-badge)](https://profi.ru/profile/DupleyMI)

> Консультации и услуги программирования на платформе Profi.ru

---

### 📚 Услуги обучения

[![Обучение технологиям и языкам программирования на Kwork](https://img.shields.io/badge/Kwork-Обучение%20Программированию-blue?style=for-the-badge&logo=kwork)](https://kwork.ru/usability-testing/42465951/obuchenie-tekhnologiyam-i-yazykam-programmirovaniya)

> Профессиональное обучение технологиям и языкам программирования. Персональные консультации и курсы от опытного преподавателя.

---

### 🏫 О школе

[![Website](https://img.shields.io/badge/Maestro7IT-school--maestro7it.ru-darkgreen?style=for-the-badge)](https://school-maestro7it.ru/)

> Инновационная школа программирования, специализирующаяся на подготовке специалистов в области современных технологий и языков программирования.
