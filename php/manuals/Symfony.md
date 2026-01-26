# 🌟 Полный мануал по Symfony: Установка, Настройка и Использование

## 📋 Содержание

1. [Введение в Symfony](#введение-в-symfony)
2. [Системные требования](#системные-требования)
3. [Установка Symfony](#установка-symfony)
4. [Базовая настройка](#базовая-настройка)
5. [Структура проекта](#структура-проекта)
6. [Конфигурация приложения](#конфигурация-приложения)
7. [Маршрутизация и контроллеры](#маршрутизация-и-контроллеры)
8. [Бандлы и сервисы](#бандлы-и-сервисы)
9. [Шаблоны Twig](#шаблоны-twig)
10. [Безопасность](#безопасность)
11. [Практические примеры](#практические-примеры)
12. [Лучшие практики](#лучшие-практики)

## Введение в Symfony

**Symfony** — это мощный PHP-фреймворк с открытым исходным кодом, который используется для создания веб-приложений и сервисов.

`Symfony` состоит из набора повторно используемых компонентов и библиотек, которые помогают разработчикам создавать масштабируемые и поддерживаемые приложения.

**Основные особенности Symfony:**

- Модульная архитектура
- Высокая производительность
- Богатая экосистема бандлов
- Встроенная система безопасности
- Мощный DI-контейнер
- Поддержка различных форматов (REST, JSON, XML)
- Отличная документация

## Системные требования

### Минимальные требования:

- **PHP:** 8.1 или выше
- **Composer:** 2.0 или выше
- **База данных:** MySQL 5.7+, PostgreSQL 11+, SQLite 3.27+, SQL Server 2019+
- **Intl PHP Extension**
- **JSON PHP Extension**
- **Ctype PHP Extension**
- **Session PHP Extension**
- **SimpleXML PHP Extension**
- **Tokenizer PHP Extension**

### Рекомендуемые требования:

- **PHP:** 8.2 или выше
- **Composer:** Последняя стабильная версия
- **Redis** или **Memcached** для кэширования
- **APCu** для кэширования
- **OPcache** для оптимизации
- **Xdebug** для отладки

## Установка Symfony

### Метод 1: Установка с помощью Symfony CLI (рекомендуется)

#### Установка Symfony CLI:

```bash
# Для Unix-систем (Linux/macOS)
curl -sS https://get.symfony.com/cli/installer | bash
sudo mv /root/.symfony/bin/symfony /usr/local/bin/symfony

# Для Windows (PowerShell)
Invoke-WebRequest https://get.symfony.com/cli/installer -OutFile installer.ps1
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
.\installer.ps1
```

#### Создание нового проекта:

```bash
symfony new my_project_directory --version=stable
```

### Метод 2: Установка с помощью Composer

#### Создание проекта с веб-панелью:

```bash
composer create-project symfony/skeleton:"^6.4" my_project
cd my_project
composer require webapp
```

#### Создание API проекта:

```bash
composer create-project symfony/skeleton:"^6.4" my_project
cd my_project
composer require api
```

### Метод 3: Установка конкретной версии

#### Установка конкретной версии Symfony:

```bash
composer create-project symfony/skeleton:"6.4.*" my_project
```

## Базовая настройка

### Настройка .env файла

**После установки Symfony, необходимо настроить файл `.env`:**

```bash
cp .env .env.local
```

**Затем отредактируйте ключевые параметры:**

```env
###> symfony/framework-bundle ###
APP_ENV=dev
APP_SECRET=fe2de9e8a7c2677c5d710e1e15a20f51
###< symfony/framework-bundle ###

###> doctrine/doctrine-bundle ###
DATABASE_URL="mysql://db_user:db_password@127.0.0.1:3306/db_name?serverVersion=8.0"
###< doctrine/doctrine-bundle ###
```

### Генерация SECRET:

```bash
symfony console secret:generate
```

## Структура проекта

```textline
project-root/
├── config/                 # Конфигурационные файлы
│   ├── packages/          # Конфигурации бандлов
│   ├── routes/            # Файлы маршрутов
│   ├── bundles.php        # Регистрация бандлов
│   ├── preload.php        # Предзагрузка классов
│   └── services.yaml      # Определение сервисов
├── public/                 # Веб-доступные файлы
│   └── index.php          # Входная точка приложения
├── src/                    # Исходный код приложения
│   ├── Controller/        # Контроллеры
│   ├── Entity/            # Сущности Doctrine
│   ├── Repository/        # Репозитории Doctrine
│   ├── Form/              # Формы
│   ├── Service/           # Сервисы приложения
│   ├── EventListener/     # Обработчики событий
│   └── Kernel.php         # Ядро приложения
├── templates/              # Шаблоны Twig
├── tests/                  # Тесты приложения
├── var/                    # Временные файлы, кэш, логи
├── vendor/                 # Зависимости Composer
├── .env                    # Переменные окружения
├── composer.json           # Зависимости проекта
└── symfony.lock            # Блокировка версий Symfony
```

## Конфигурация приложения

### Основные конфигурационные файлы:

#### config/packages/framework.yaml:

```yaml
framework:
    secret: '%env(APP_SECRET)%'
    #csrf_protection: true
    http_method_override: false

    # Enables session support. Note that the session will ONLY be started if you read or write from it.
    session:
        handler_id: null
        cookie_secure: auto
        cookie_samesite: lax
        storage_factory_id: session.storage.factory.native

    #esi: true
    #fragments: true
    php_errors:
        log: true
```

#### config/packages/doctrine.yaml:

```yaml
doctrine:
    dbal:
        url: '%env(resolve:DATABASE_URL)%'

        # IMPORTANT: You MUST configure your server version,
        # either here or in the DATABASE_URL env var (see .env file)
        #server_version: '15'
    orm:
        auto_generate_proxy_classes: true
        naming_strategy: doctrine.orm.naming_strategy.underscore_number_aware
        auto_mapping: true
        mappings:
            App:
                is_bundle: false
                dir: '%kernel.project_dir%/src/Entity'
                prefix: 'App\Entity'
                alias: App
```

## Маршрутизация и контроллеры

### Определение маршрутов:

#### config/routes.yaml:

```yaml
controllers:
    resource:
        path: ../src/Controller/
        namespace: App\Controller
    type: attribute

kernel:
    resource: App\Kernel
    type: attribute
```

### Создание контроллера:

```bash
symfony console make:controller BlogController
```

#### Пример контроллера:

```php
<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class BlogController extends AbstractController
{
    #[Route('/blog', name: 'app_blog')]
    public function index(): Response
    {
        return $this->render('blog/index.html.twig', [
            'controller_name' => 'BlogController',
        ]);
    }

    #[Route('/blog/{id}', name: 'app_blog_show', requirements: ['id' => '\d+'])]
    public function show(int $id): Response
    {
        return $this->render('blog/show.html.twig', [
            'id' => $id,
        ]);
    }
}
```

### Альтернативный способ с аннотациями (для старых версий):

```php
<?php

use Symfony\Component\Routing\Annotation\Route;

/**
 * @Route("/blog")
 */
class BlogController extends AbstractController
{
    /**
     * @Route("/", name="app_blog")
     */
    public function index(): Response
    {
        // ...
    }
}
```

## Бандлы и сервисы

### Установка популярных бандлов:

```bash
# Maker bundle для генерации кода
composer require --dev symfony/maker-bundle

# Security bundle
composer require symfony/security-bundle

# Twig bundle
composer require symfony/twig-bundle

# Form bundle
composer require symfony/form

# Validator bundle
composer require symfony/validator

# Translation bundle
composer require symfony/translation

# Mailer bundle
composer require symfony/mailer
```

### Регистрация бандлов (config/bundles.php):

```php
<?php

return [
    Symfony\Bundle\FrameworkBundle\FrameworkBundle::class => ['all' => true],
    Symfony\Bundle\TwigBundle\TwigBundle::class => ['all' => true],
    Symfony\Bundle\SecurityBundle\SecurityBundle::class => ['all' => true],
    Doctrine\Bundle\DoctrineBundle\DoctrineBundle::class => ['all' => true],
    Symfony\Bundle\MakerBundle\MakerBundle::class => ['dev' => true],
];
```

### Определение сервисов (config/services.yaml):

```yaml
services:
    # Default configuration for services
    _defaults:
        autowire: true      # Automatically injects dependencies in your services
        autoconfigure: true # Automatically registers your services as commands, event subscribers, etc.

    App\:
        resource: '../src/'
        exclude:
            - '../src/DependencyInjection/'
            - '../src/Entity/'
            - '../src/Kernel.php'
```

## Шаблоны Twig

### Основной шаблон (templates/base.html.twig):

```twig
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>{% block title %}Welcome!{% endblock %}</title>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 128 128%22><text y=%221.2em%22 font-size=%2296%22>⚫️</text></svg>">
        {% block stylesheets %}{% endblock %}
    </head>
    <body>
        {% block body %}{% endblock %}
        {% block javascripts %}{% endblock %}
    </body>
</html>
```

### Дочерний шаблон:

```twig
{% extends 'base.html.twig' %}

{% block title %}Blog posts{% endblock %}

{% block body %}
<div class="container">
    <h1>Latest blog posts</h1>
    
    {% for post in posts %}
        <div class="post">
            <h2>{{ post.title }}</h2>
            <p>{{ post.content|striptags|u.truncate(100) }}</p>
            <a href="{{ path('app_blog_show', {'id': post.id}) }}">Read more</a>
        </div>
    {% endfor %}
</div>
{% endblock %}
```

## Безопасность

### Конфигурация безопасности (config/packages/security.yaml):

```yaml
security:
    # https://symfony.com/doc/current/security.html#registering-the-user-hashing-passwords
    password_hashers:
        Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface: 'auto'
    
    # https://symfony.com/doc/current/security.html#loading-the-user-the-user-provider
    providers:
        users_in_memory: { memory: null }
    
    firewalls:
        dev:
            pattern: ^/(_(profiler|wdt)|css|images|js)/
            security: false
        main:
            lazy: true
            provider: users_in_memory
            custom_authenticator: App\Security\AppCustomAuthenticator
            logout:
                path: app_logout
                # where to redirect after logout
                # target: app_any_route

            # activate different ways to authenticate
            # https://symfony.com/doc/current/security.html#the-firewall

            # https://symfony.com/doc/current/security/impersonating_user.html
            # switch_user: true

    # Easy way to control access for large sections of your site
    # Note: Only the *first* access control that matches will be used
    access_control:
        # - { path: ^/admin, roles: ROLE_ADMIN }
        # - { path: ^/profile, roles: ROLE_USER }
```

### Защита маршрутов:

```php
#[Route('/admin', name: 'admin')]
#[IsGranted('ROLE_ADMIN')]
public function admin(): Response
{
    // Только пользователи с ролью ADMIN могут получить доступ
}
```

## Практические примеры

### Пример №1: Создание CRUD приложения

#### 1. Создайте сущность:

```bash
symfony console make:entity Article
```

#### 2. Определите поля:

```php
<?php

namespace App\Entity;

use App\Repository\ArticleRepository;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: ArticleRepository::class)]
class Article
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    private ?string $title = null;

    #[ORM\Column(type: 'text')]
    private ?string $content = null;

    #[ORM\Column(type: 'datetime_immutable')]
    private ?\DateTimeImmutable $createdAt = null;

    public function __construct()
    {
        $this->createdAt = new \DateTimeImmutable();
    }

    // Getters and setters...
}
```

#### 3. Создайте контроллер:

```bash
symfony console make:controller ArticleController
```

#### 4. Реализуйте методы контроллера:

```php
<?php

namespace App\Controller;

use App\Entity\Article;
use App\Form\ArticleType;
use App\Repository\ArticleRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/article')]
class ArticleController extends AbstractController
{
    #[Route('/', name: 'app_article_index', methods: ['GET'])]
    public function index(ArticleRepository $articleRepository): Response
    {
        return $this->render('article/index.html.twig', [
            'articles' => $articleRepository->findAll(),
        ]);
    }

    #[Route('/new', name: 'app_article_new', methods: ['GET', 'POST'])]
    public function new(Request $request, ArticleRepository $articleRepository): Response
    {
        $article = new Article();
        $form = $this->createForm(ArticleType::class, $article);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $articleRepository->save($article, true);

            return $this->redirectToRoute('app_article_index', [], Response::HTTP_SEE_OTHER);
        }

        return $this->renderForm('article/new.html.twig', [
            'article' => $article,
            'form' => $form,
        ]);
    }
}
```

### Пример №2: Работа с формами

```php
<?php

namespace App\Form;

use App\Entity\Article;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class ArticleType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('title')
            ->add('content')
        ;
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => Article::class,
        ]);
    }
}
```

### Пример №3: Использование команд Symfony

```bash
# Запуск сервера разработки
symfony serve

# Запуск команды консоли
symfony console cache:clear

# Генерация кода
symfony console make:controller MyController
symfony console make:entity MyEntity
symfony console make:migration
```

## Лучшие практики

### 1. Используйте Dependency Injection

```php
class ArticleService
{
    public function __construct(
        private EntityManagerInterface $entityManager,
        private ArticleRepository $articleRepository
    ) {}
}
```

### 2. Используйте Value Objects для сложной логики

```php
readonly class ArticleTitle
{
    public function __construct(
        private string $title
    ) {
        if (strlen($title) > 255) {
            throw new InvalidArgumentException('Title too long');
        }
    }

    public function toString(): string
    {
        return $this->title;
    }
}
```

### 3. Используйте DTO для передачи данных

```php
class CreateArticleDTO
{
    public function __construct(
        public readonly string $title,
        public readonly string $content,
        public readonly array $tags = [],
    ) {}
}
```

### 4. Организуйте код по функциональностям

```
src/
├── Blog/
│   ├── Entity/
│   ├── Repository/
│   ├── Controller/
│   └── Service/
└── User/
    ├── Entity/
    ├── Repository/
    ├── Controller/
    └── Service/
```

### 5. Используйте события Symfony

```php
use Symfony\Contracts\EventDispatcher\Event;

class ArticleCreatedEvent extends Event
{
    public function __construct(public readonly Article $article) {}
}
```

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
[![Обучение технологиям и языкам программирования на Kwork](https://img.shields.io/badge/Kwork-Обучение%20Программированию-blue?style=for-the-badge&logo=kwork)](https://kwork.ru/usability-testing/42465951/obuchenie-tekhnologiyam-i-yazykam-programmirovaniya)

> Профессиональное обучение технологиям и языкам программирования. Персональные консультации и курсы от опытного преподавателя.

---

### 🏫 О школе
[![Website](https://img.shields.io/badge/Maestro7IT-school--maestro7it.ru-darkgreen?style=for-the-badge)](https://school-maestro7it.ru/)

> Инновационная школа программирования, специализирующаяся на подготовке специалистов в области современных технологий и языков программирования.