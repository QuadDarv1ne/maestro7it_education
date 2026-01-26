# Полный мануал по Laravel: Установка, Настройка и Использование

## 📋 Содержание

1. [Введение в Laravel](#введение-в-laravel)
2. [Системные требования](#системные-требования)
3. [Установка Laravel](#установка-laravel)
4. [Базовая настройка](#базовая-настройка)
5. [Структура проекта](#структура-проекта)
6. [Конфигурация приложения](#конфигурация-приложения)
7. [Маршруты и контроллеры](#маршруты-и-контроллеры)
8. [Миграции и модели](#миграции-и-модели)
9. [Blade шаблоны](#blade-шаблоны)
10. [Аутентификация](#аутентификация)
11. [Практические примеры](#практические-примеры)
12. [Лучшие практики](#лучшие-практики)

## Введение в Laravel

**Laravel** — это мощный PHP-фреймворк с открытым исходным кодом, предназначенный для разработки веб-приложений, следуя архитектурному паттерну `Model-View-Controller (MVC)` 

`Laravel` предоставляет богатый набор возможностей для ускорения разработки, включая инструменты для аутентификации, маршрутизации, сессий и управления кэшем.

**Основные особенности Laravel:**

- Элегантный и чистый синтаксис
- Мощная `ORM` (`Eloquent`)
- Встроенная система аутентификации
- Миграции баз данных
- `Middleware` для защиты
- Встроенная система тестирования
- Потрясающая документация

## Системные требования

### Минимальные требования:

- **PHP:** 8.1 или выше
- **Composer:** 2.2 или выше
- **База данных:** MySQL 5.7+, PostgreSQL 9.6+, SQLite 3.8.8+, SQL Server 2017+
- **OpenSSL PHP Extension**
- **PDO PHP Extension**
- **Mbstring PHP Extension**
- **Tokenizer PHP Extension**
- **XML PHP Extension**
- **Ctype PHP Extension**
- **JSON PHP Extension**

### Рекомендуемые требования:

- **PHP:** 8.2 или выше
- **Composer:** Последняя стабильная версия
- **Redis** или **Memcached** для кэширования
- **Queue worker** (Redis или Database)
- **Mail server** (SMTP)

## Установка Laravel

### Метод 1: Установка с помощью Composer (рекомендуется)

#### Установка Laravel Installer:

```bash
composer global require laravel/installer
```

#### Создание нового проекта:

```bash
laravel new project-name

# Или через Composer:
composer create-project laravel/laravel project-name
```

### Метод 2: Установка с определенной версией

#### Установка конкретной версии Laravel:

```bash
composer create-project laravel/laravel:^10.0 project-name
```

### Метод 3: Установка с помощью Git

#### Клонирование шаблона:

```bash
git clone https://github.com/laravel/laravel.git project-name
cd project-name
composer install
```

## Базовая настройка

### Настройка .env файла

После установки Laravel, необходимо настроить файл `.env`:

```bash
cp .env.example .env
```

**Затем отредактируйте ключевые параметры:**

```env
APP_NAME=Laravel
APP_ENV=local
APP_KEY=
APP_DEBUG=true
APP_URL=http://localhost

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=

BROADCAST_DRIVER=log
CACHE_DRIVER=file
QUEUE_CONNECTION=sync
SESSION_DRIVER=file
SESSION_LIFETIME=120

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379
```

### Генерация APP_KEY:

```bash
php artisan key:generate
```

## Структура проекта

```printtext
project-root/
├── app/                    # Основной код приложения
│   ├── Console/           # Команды Artisan
│   ├── Exceptions/        # Обработка исключений
│   ├── Http/              # Контроллеры, middleware, запросы
│   ├── Models/            # Модели Eloquent
│   ├── Providers/         # Service providers
│   └── Services/          # Кастомные сервисы
├── bootstrap/             # Файлы загрузки фреймворка
├── config/                # Конфигурационные файлы
├── database/              # Миграции, фикстуры, фабрики
├── public/                # Веб-доступные файлы и ресурсы
├── resources/             # Шаблоны, ассеты, локализация
├── routes/                # Файлы маршрутов
├── storage/               # Файлы кэша, сессий, загрузок
├── tests/                 # Тесты приложения
├── vendor/                # Зависимости Composer
├── .env                   # Переменные окружения
├── artisan                # Консольный интерфейс
├── composer.json          # Зависимости проекта
└── package.json           # Frontend зависимости
```

## Конфигурация приложения

### Основные конфигурационные файлы:

#### app.php - Основная конфигурация

```php
<?php

return [
    'name' => env('APP_NAME', 'Laravel'),
    'env' => env('APP_ENV', 'production'),
    'debug' => (bool) env('APP_DEBUG', false),
    'url' => env('APP_URL', 'http://localhost'),
    'timezone' => 'UTC',
    'locale' => 'en',
];
```

#### database.php - Конфигурация базы данных

```php
<?php

return [
    'default' => env('DB_CONNECTION', 'mysql'),
    'connections' => [
        'mysql' => [
            'driver' => 'mysql',
            'url' => env('DATABASE_URL'),
            'host' => env('DB_HOST', '127.0.0.1'),
            'port' => env('DB_PORT', '3306'),
            'database' => env('DB_DATABASE', 'forge'),
            'username' => env('DB_USERNAME', 'forge'),
            'password' => env('DB_PASSWORD', ''),
        ],
    ],
];
```

## Маршруты и контроллеры

### Определение маршрутов:

#### routes/web.php:

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PostController;

Route::get('/', function () {
    return view('welcome');
});

Route::resource('posts', PostController::class);

Route::prefix('api')->group(function () {
    Route::get('/users', [UserController::class, 'index']);
});
```

### Создание контроллера:

```bash
php artisan make:controller PostController
```

#### Пример контроллера:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function index()
    {
        $posts = Post::all();
        return view('posts.index', compact('posts'));
    }

    public function show(Post $post)
    {
        return view('posts.show', compact('post'));
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'content' => 'required',
        ]);

        Post::create($validated);
        
        return redirect()->route('posts.index');
    }
}
```

## Миграции и модели

### Создание миграции:

```bash
php artisan make:migration create_posts_table
```

#### Пример миграции:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();
            $table->string('title');
            $table->text('content');
            $table->foreignId('user_id')->constrained();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('posts');
    }
};
```

### Создание модели:

```bash
php artisan make:model Post
```

#### Пример модели:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    use HasFactory;

    protected $fillable = [
        'title',
        'content',
        'user_id',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

## Blade шаблоны

### Основной шаблон (resources/views/layouts/app.blade.php):

```blade
<!DOCTYPE html>
<html>
<head>
    <title>{{ config('app.name') }}</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    <nav>
        <!-- Navigation -->
    </nav>

    <main>
        @yield('content')
    </main>

    @stack('scripts')
</body>
</html>
```

### Дочерний шаблон:

```blade
@extends('layouts.app')

@section('content')
<div class="container">
    <h1>Posts</h1>
    
    @foreach($posts as $post)
        <div class="post">
            <h2>{{ $post->title }}</h2>
            <p>{{ Str::limit($post->content, 100) }}</p>
            <a href="{{ route('posts.show', $post) }}">Read More</a>
        </div>
    @endforeach
</div>
@endsection
```

## Аутентификация

### Установка Laravel Breeze (рекомендуемый способ):

```bash
composer require laravel/breeze --dev
php artisan breeze:install
npm install && npm run build
```

### Или установка вручную:

```bash
php artisan make:auth
```

### Защита маршрутов:

```php
Route::middleware('auth')->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
});
```

## Практические примеры

### Пример 1: Создание CRUD приложения

#### 1. Создайте модель и миграцию:

```bash
php artisan make:model Article -m
```

#### 2. Определите поля в миграции:

```php
public function up()
{
    Schema::create('articles', function (Blueprint $table) {
        $table->id();
        $table->string('title');
        $table->text('content');
        $table->boolean('published')->default(false);
        $table->timestamps();
    });
}
```

#### 3. Запустите миграцию:

```bash
php artisan migrate
```

#### 4. Создайте контроллер:

```bash
php artisan make:controller ArticleController --resource
```

#### 5. Реализуйте методы контроллера:

```php
class ArticleController extends Controller
{
    public function index()
    {
        $articles = Article::all();
        return view('articles.index', compact('articles'));
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'content' => 'required',
        ]);

        Article::create($validated);

        return redirect()->route('articles.index')
                        ->with('success', 'Article created successfully.');
    }
    
    // другие методы...
}
```

### Пример 2: Работа с Eloquent ORM

```php
// Получение всех записей
$articles = Article::all();

// Получение одной записи
$article = Article::find(1);

// Фильтрация с условиями
$publishedArticles = Article::where('published', true)->get();

// Создание новой записи
Article::create([
    'title' => 'New Article',
    'content' => 'Article content...',
]);

// Обновление записи
$article->update(['title' => 'Updated Title']);

// Удаление записи
$article->delete();
```

### Пример 3: Использование Artisan команд

```bash
# Запуск сервера разработки
php artisan serve

# Очистка кэша
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear

# Запуск тестов
php artisan test

# Запуск очередей
php artisan queue:work
```

## Лучшие практики

### 1. Используйте Eloquent вместо Query Builder когда возможно

```php
// Хорошо
$users = User::where('active', true)->get();

// Лучше (если нужно много связанных данных)
$users = User::with('posts')->where('active', true)->get();
```

### 2. Используйте Form Request для валидации

```php
php artisan make:request StorePostRequest

// В файле StorePostRequest.php
public function rules()
{
    return [
        'title' => 'required|string|max:255',
        'content' => 'required|string',
    ];
}
```

### 3. Используйте Resource для API ответов

```php
use App\Http\Resources\PostResource;

public function index()
{
    $posts = Post::all();
    return PostResource::collection($posts);
}
```

### 4. Используйте Factories для тестирования

```php
// database/factories/UserFactory.php
protected $model = User::class;

public function definition()
{
    return [
        'name' => $this->faker->name(),
        'email' => $this->faker->unique()->safeEmail(),
    ];
}
```

### 5. Организуйте код по namespace

- Controllers в `App\Http\Controllers`
- Models в `App\Models`
- Services в `App\Services`
- Helpers в `App\Helpers`

---

#### 💼 Автор: Дуплей Максим Игоревич

#### 📲 Контакты:
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