# Работа с веб-приложениями на ASP.NET Core

**ASP.NET Core** — это кросс-платформенный фреймворк для создания современных веб-приложений и `API`.

Он предлагает высокую производительность, модульность и поддержку различных платформ.

### Введение в ASP.NET Core

**ASP.NET Core** — это фреймворк, который позволяет создавать веб-приложения и `API`.

Он разработан для работы на различных платформах, таких как `Windows`, `macOS` и `Linux`.

`ASP.NET Core` объединяет лучшие возможности `ASP.NET` и улучшает их, предлагая модульную архитектуру, поддержку кросс-платформенных решений и другие преимущества.

**Ключевые особенности ASP.NET Core:**

- Кросс-платформенность.
- Модульная архитектура.
- Интеграция с современными инструментами и библиотеками.
- Высокая производительность.
- Создание простого веб-приложения

**Создание проекта:**

В Visual Studio выберите `"Создать новый проект"`, затем выберите `"ASP.NET Core Web Application"`.

Выберите шаблон `"Web Application (Model-View-Controller)"` для создания `MVC-приложения` или `"Web Application"` для `Razor Pages`.

**Структура проекта:**

**Основные папки и файлы проекта:**

- `Controllers/`: Контроллеры для обработки запросов.
- `Views/`: Шаблоны представлений для отображения данных.
- `Models/`: Модели данных.
- `wwwroot/`: Статические файлы (CSS, JavaScript, изображения).
- `Program.cs` и `Startup.cs`: Конфигурация приложения.

**Пример создания контроллера и представления:**

**Создание контроллера:**

**В папке `Controllers` создайте файл `HomeController.cs`:**

```csharp
using Microsoft.AspNetCore.Mvc;

namespace MyWebApp.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }

        public IActionResult About()
        {
            ViewData["Message"] = "Your application description page.";
            return View();
        }
    }
}
```

**Создание представлений:**

**В папке `Views/Home` создайте файл `Index.cshtml`:**

```html
@*
  Главная страница приложения.
*@
<h1>Welcome to My Web App!</h1>
```

**В папке `Views/Home` создайте файл `About.cshtml`:**

```html
@*
  Страница "О нас".
*@
<h1>About</h1>
<p>@ViewData["Message"]</p>
```

**Настройка маршрутизации:**

**В файле `Startup.cs` настройте маршрутизацию:**

```csharp
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddControllersWithViews();
    }

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        if (env.IsDevelopment())
        {
            app.UseDeveloperExceptionPage();
        }
        else
        {
            app.UseExceptionHandler("/Home/Error");
            app.UseHsts();
        }

        app.UseHttpsRedirection();
        app.UseStaticFiles();

        app.UseRouting();

        app.UseAuthorization();

        app.UseEndpoints(endpoints =>
        {
            endpoints.MapControllerRoute(
                name: "default",
                pattern: "{controller=Home}/{action=Index}/{id?}");
        });
    }
}
```

### Взаимодействие с базами данных через Entity Framework

**Entity Framework Core (EF Core)** — это объектно-реляционный маппер (ORM), который позволяет работать с базами данных в .NET-приложениях, используя объектно-ориентированный подход.

#### 1. Установка пакета EF Core

**В проекте установите пакеты `EF` Core через `NuGet`:**

```csharp
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Tools
```

#### 2. Создание модели данных

**В папке `Models` создайте класс модели, например, `Product.cs`:**

```csharp
namespace MyWebApp.Models
{
    public class Product
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public decimal Price { get; set; }
    }
}
```

#### 3. Создание контекста базы данных

**В папке Models создайте класс контекста, например, `ApplicationDbContext.cs`:**

```csharp
using Microsoft.EntityFrameworkCore;

namespace MyWebApp.Models
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<Product> Products { get; set; }
    }
}
```

#### 4. Настройка контекста в `Startup.cs`

```csharp
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseSqlServer(Configuration.GetConnectionString("DefaultConnection")));
        services.AddControllersWithViews();
    }

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        // Настройки как ранее
    }
}
```

#### 5. Создание миграций и обновление базы данных

**Используйте команду для создания миграции и обновления базы данных:**

```sql
dotnet ef migrations add InitialCreate
dotnet ef database update
```

Эти команды создадут схему базы данных на основе моделей данных и применят изменения.

#### 6. Работа с данными

**В контроллере добавьте логику для работы с данными:**

```csharp
using Microsoft.AspNetCore.Mvc;
using MyWebApp.Models;
using System.Linq;

namespace MyWebApp.Controllers
{
    public class ProductsController : Controller
    {
        private readonly ApplicationDbContext _context;

        public ProductsController(ApplicationDbContext context)
        {
            _context = context;
        }

        public IActionResult Index()
        {
            var products = _context.Products.ToList();
            return View(products);
        }
    }
}
```

**Создание представления для Products:**

В папке `Views/Products` создайте файл `Index.cshtml`:

```html
@model IEnumerable<MyWebApp.Models.Product>

<h1>Products</h1>
<ul>
    @foreach (var product in Model)
    {
        <li>@product.Name - @product.Price</li>
    }
</ul>
```

### Резюме

`ASP.NET Core` позволяет создавать мощные веб-приложения и `API`.

`Entity Framework Core` упрощает работу с базами данных, предоставляя `ORM-решение` для `.NET-приложений`.

Создание веб-приложения в `ASP.NET Core` включает создание контроллеров, представлений и настройку маршрутизации.

Для работы с базами данных через `EF Core` необходимо настроить контекст, создать модели данных и управлять миграциями.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия:** 1.0