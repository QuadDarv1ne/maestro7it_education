# 🚀 C# Frameworks: Полное руководство по популярным фреймворкам и библиотекам

## 📋 Содержание

1. [Введение в C# фреймворки](#введение-в-c-фреймворки)
2. [Веб-фреймворки](#веб-фреймворки)
3. [Desktop фреймворки](#desktop-фреймворки)
4. [Мобильные фреймворки](#мобильные-фреймворки)
5. [ORM и работа с данными](#orm-и-работа-с-данными)
6. [Тестирование](#тестирование)
7. [Утилитарные библиотеки](#утилитарные-библиотеки)
8. [Выбор подходящего фреймворка](#выбор-подходящего-фреймворка)
9. [Практические примеры](#практические-примеры)

## Введение в C# фреймворки

**C# фреймворк** — это набор библиотек, инструментов и соглашений, которые упрощают разработку приложений на `C#`

Они предоставляют готовые решения для типичных задач и позволяют сосредоточиться на бизнес-логике.

### Экосистема .NET

**.NET** — это свободная, кроссплатформенная среда разработки, поддерживающая несколько языков программирования, включая `C#`

**Основные компоненты .NET:**
- **.NET Runtime**: Среда выполнения
- **Base Class Library (BCL)**: Базовые классы
- **SDK**: Инструменты разработки
- **Фреймворки**: ASP.NET, Entity Framework и др.

### Преимущества использования фреймворков:
- **Ускорение разработки**: Готовые компоненты
- **Стандартизация**: Единый стиль кода
- **Надежность**: Протестированные решения
- **Поддержка сообщества**: Документация и помощь
- **Кроссплатформенность**: Работа на разных ОС

---

## Веб-фреймворки

### 1. ASP.NET Core

**Описание**: Современный кроссплатформенный фреймворк для создания веб-приложений и `API`

**Особенности**:
- Кроссплатформенность (`Windows`, `Linux`, `macOS`)
- Высокая производительность
- Встроенная поддержка Dependency Injection
- Middleware архитектура
- Встроенная поддержка `HTTPS`
- Интеграция с `Docker`

**Установка**:
```bash
# Установка .NET SDK
# Скачать с https://dotnet.microsoft.com/download

# Создание нового веб-приложения
dotnet new webapp -n MyWebApp
cd MyWebApp
dotnet run
```

**Пример простого API**:
```csharp
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);

// Добавление сервисов
builder.Services.AddControllers();

var app = builder.Build();

// Middleware
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}

app.UseHttpsRedirection();
app.UseRouting();
app.UseAuthorization();

app.MapControllers();

app.Run();
```

**Контроллер API**:
```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("[controller]")]
public class WeatherForecastController : ControllerBase
{
    private static readonly string[] Summaries = new[]
    {
        "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
    };

    [HttpGet]
    public IEnumerable<WeatherForecast> Get()
    {
        return Enumerable.Range(1, 5).Select(index => new WeatherForecast
        {
            Date = DateTime.Now.AddDays(index),
            TemperatureC = Random.Shared.Next(-20, 55),
            Summary = Summaries[Random.Shared.Next(Summaries.Length)]
        })
        .ToArray();
    }
}

public class WeatherForecast
{
    public DateTime Date { get; set; }
    public int TemperatureC { get; set; }
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
    public string? Summary { get; set; }
}
```

### 2. Blazor

**Описание**: Фреймворк для создания интерактивных веб-приложений с использованием `C#` вместо `JavaScript`

**Типы Blazor**:
- **Blazor Server**: Приложение выполняется на сервере
- **Blazor WebAssembly**: Приложение выполняется в браузере
- **Blazor Hybrid**: Комбинация с `MAUI` для десктоп/мобильных приложений

**Пример компонента Blazor**:
```razor
@page "/counter"

<h1>Счетчик</h1>

<p>Текущий счет: @currentCount</p>

<button class="btn btn-primary" @onclick="IncrementCount">Нажми меня</button>

@code {
    private int currentCount = 0;

    private void IncrementCount()
    {
        currentCount++;
    }
}
```

**Установка Blazor**:
```bash
# Создание Blazor WebAssembly приложения
dotnet new blazorwasm -n MyBlazorApp
cd MyBlazorApp
dotnet run
```

### 3. Minimal API

**Описание**: Упрощенный способ создания `API` без использования контроллеров.

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var summaries = new[]
{
    "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
};

app.MapGet("/weatherforecast", () =>
{
    var forecast = Enumerable.Range(1, 5).Select(index =>
        new WeatherForecast
        (
            DateTime.Now.AddDays(index),
            Random.Shared.Next(-20, 55),
            summaries[Random.Shared.Next(summaries.Length)]
        ))
        .ToArray();
    return forecast;
});

app.Run();

internal record WeatherForecast(DateTime Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}
```

---

## Desktop фреймворки

### 1. WPF (Windows Presentation Foundation)

**Описание**: Современный фреймворк для создания десктопных приложений на `Windows`

**Особенности**:
- Декларативный `XAML` для `UI`
- Привязка данных (`Data Binding`)
- Стили и шаблоны
- `2D/3D` графика
- Анимации

**Пример приложения WPF**:
```xml
<!-- MainWindow.xaml -->
<Window x:Class="WpfApp.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Калькулятор" Height="350" Width="300">
    <Grid Margin="10">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        
        <TextBox Grid.Row="0" Name="Display" 
                 FontSize="24" HorizontalContentAlignment="Right"
                 IsReadOnly="True"/>
        
        <UniformGrid Grid.Row="1" Rows="4" Columns="4" Margin="0,10,0,0">
            <Button Content="7" Click="Number_Click"/>
            <Button Content="8" Click="Number_Click"/>
            <Button Content="9" Click="Number_Click"/>
            <Button Content="/" Click="Operator_Click"/>
            
            <Button Content="4" Click="Number_Click"/>
            <Button Content="5" Click="Number_Click"/>
            <Button Content="6" Click="Number_Click"/>
            <Button Content="*" Click="Operator_Click"/>
            
            <Button Content="1" Click="Number_Click"/>
            <Button Content="2" Click="Number_Click"/>
            <Button Content="3" Click="Number_Click"/>
            <Button Content="-" Click="Operator_Click"/>
            
            <Button Content="0" Click="Number_Click"/>
            <Button Content="." Click="Decimal_Click"/>
            <Button Content="=" Click="Equals_Click"/>
            <Button Content="+" Click="Operator_Click"/>
        </UniformGrid>
        
        <Button Grid.Row="2" Content="Очистить" 
                Margin="0,10,0,0" Click="Clear_Click"/>
    </Grid>
</Window>
```

```csharp
// MainWindow.xaml.cs
using System;
using System.Windows;

namespace WpfApp
{
    public partial class MainWindow : Window
    {
        private double currentValue = 0;
        private string pendingOperation = "";
        private bool isNewOperation = true;

        public MainWindow()
        {
            InitializeComponent();
            Display.Text = "0";
        }

        private void Number_Click(object sender, RoutedEventArgs e)
        {
            string number = ((System.Windows.Controls.Button)sender).Content.ToString();
            
            if (isNewOperation)
            {
                Display.Text = number;
                isNewOperation = false;
            }
            else
            {
                Display.Text += number;
            }
        }

        private void Operator_Click(object sender, RoutedEventArgs e)
        {
            string operation = ((System.Windows.Controls.Button)sender).Content.ToString();
            
            if (!string.IsNullOrEmpty(pendingOperation))
            {
                Calculate();
            }
            
            pendingOperation = operation;
            currentValue = double.Parse(Display.Text);
            isNewOperation = true;
        }

        private void Equals_Click(object sender, RoutedEventArgs e)
        {
            Calculate();
            pendingOperation = "";
            isNewOperation = true;
        }

        private void Clear_Click(object sender, RoutedEventArgs e)
        {
            Display.Text = "0";
            currentValue = 0;
            pendingOperation = "";
            isNewOperation = true;
        }

        private void Decimal_Click(object sender, RoutedEventArgs e)
        {
            if (isNewOperation)
            {
                Display.Text = "0.";
                isNewOperation = false;
            }
            else if (!Display.Text.Contains("."))
            {
                Display.Text += ".";
            }
        }

        private void Calculate()
        {
            double newValue = double.Parse(Display.Text);
            
            switch (pendingOperation)
            {
                case "+":
                    currentValue += newValue;
                    break;
                case "-":
                    currentValue -= newValue;
                    break;
                case "*":
                    currentValue *= newValue;
                    break;
                case "/":
                    if (newValue != 0)
                        currentValue /= newValue;
                    else
                        Display.Text = "Ошибка";
                    break;
            }
            
            Display.Text = currentValue.ToString();
        }
    }
}
```

### 2. WinForms

**Описание**: Традиционный фреймворк для создания десктопных приложений на `Windows`

**Особенности**:
- Простота использования
- Большое количество готовых контролов
- Подходит для простых приложений
- Меньше ресурсов, чем `WPF`

**Пример WinForms приложения**:
```csharp
using System;
using System.Drawing;
using System.Windows.Forms;

public class CalculatorForm : Form
{
    private TextBox display;
    private Button[] numberButtons = new Button[10];
    private Button addButton, subtractButton, multiplyButton, divideButton;
    private Button equalsButton, clearButton, decimalButton;
    
    private double currentValue = 0;
    private string pendingOperation = "";
    private bool isNewOperation = true;

    public CalculatorForm()
    {
        InitializeComponents();
    }

    private void InitializeComponents()
    {
        this.Text = "Калькулятор";
        this.Size = new Size(300, 400);
        this.StartPosition = FormStartPosition.CenterScreen;

        // Дисплей
        display = new TextBox();
        display.Location = new Point(20, 20);
        display.Size = new Size(240, 30);
        display.Font = new Font("Arial", 16);
        display.TextAlign = HorizontalAlignment.Right;
        display.ReadOnly = true;
        display.Text = "0";
        this.Controls.Add(display);

        // Кнопки цифр
        int x = 20, y = 70;
        for (int i = 1; i <= 9; i++)
        {
            numberButtons[i] = new Button();
            numberButtons[i].Text = i.ToString();
            numberButtons[i].Location = new Point(x, y);
            numberButtons[i].Size = new Size(50, 50);
            numberButtons[i].Font = new Font("Arial", 14);
            numberButtons[i].Click += Number_Click;
            this.Controls.Add(numberButtons[i]);
            
            x += 60;
            if (i % 3 == 0)
            {
                x = 20;
                y += 60;
            }
        }

        // Кнопка 0
        numberButtons[0] = new Button();
        numberButtons[0].Text = "0";
        numberButtons[0].Location = new Point(20, 250);
        numberButtons[0].Size = new Size(110, 50);
        numberButtons[0].Font = new Font("Arial", 14);
        numberButtons[0].Click += Number_Click;
        this.Controls.Add(numberButtons[0]);

        // Операторы
        addButton = CreateOperatorButton("+", 200, 70);
        subtractButton = CreateOperatorButton("-", 200, 130);
        multiplyButton = CreateOperatorButton("*", 200, 190);
        divideButton = CreateOperatorButton("/", 200, 250);

        // Кнопки = и очистить
        equalsButton = new Button();
        equalsButton.Text = "=";
        equalsButton.Location = new Point(140, 250);
        equalsButton.Size = new Size(50, 50);
        equalsButton.Font = new Font("Arial", 14);
        equalsButton.Click += Equals_Click;
        this.Controls.Add(equalsButton);

        clearButton = new Button();
        clearButton.Text = "C";
        clearButton.Location = new Point(20, 310);
        clearButton.Size = new Size(230, 30);
        clearButton.Click += Clear_Click;
        this.Controls.Add(clearButton);

        decimalButton = new Button();
        decimalButton.Text = ".";
        decimalButton.Location = new Point(140, 310);
        decimalButton.Size = new Size(50, 30);
        decimalButton.Click += Decimal_Click;
        this.Controls.Add(decimalButton);
    }

    private Button CreateOperatorButton(string text, int x, int y)
    {
        Button button = new Button();
        button.Text = text;
        button.Location = new Point(x, y);
        button.Size = new Size(50, 50);
        button.Font = new Font("Arial", 14);
        button.Click += Operator_Click;
        this.Controls.Add(button);
        return button;
    }

    private void Number_Click(object sender, EventArgs e)
    {
        string number = ((Button)sender).Text;
        
        if (isNewOperation)
        {
            display.Text = number;
            isNewOperation = false;
        }
        else
        {
            display.Text += number;
        }
    }

    private void Operator_Click(object sender, EventArgs e)
    {
        string operation = ((Button)sender).Text;
        
        if (!string.IsNullOrEmpty(pendingOperation))
        {
            Calculate();
        }
        
        pendingOperation = operation;
        currentValue = double.Parse(display.Text);
        isNewOperation = true;
    }

    private void Equals_Click(object sender, EventArgs e)
    {
        Calculate();
        pendingOperation = "";
        isNewOperation = true;
    }

    private void Clear_Click(object sender, EventArgs e)
    {
        display.Text = "0";
        currentValue = 0;
        pendingOperation = "";
        isNewOperation = true;
    }

    private void Decimal_Click(object sender, EventArgs e)
    {
        if (isNewOperation)
        {
            display.Text = "0.";
            isNewOperation = false;
        }
        else if (!display.Text.Contains("."))
        {
            display.Text += ".";
        }
    }

    private void Calculate()
    {
        double newValue = double.Parse(display.Text);
        
        switch (pendingOperation)
        {
            case "+":
                currentValue += newValue;
                break;
            case "-":
                currentValue -= newValue;
                break;
            case "*":
                currentValue *= newValue;
                break;
            case "/":
                if (newValue != 0)
                    currentValue /= newValue;
                else
                    display.Text = "Ошибка";
                break;
        }
        
        display.Text = currentValue.ToString();
    }

    [STAThread]
    public static void Main()
    {
        Application.EnableVisualStyles();
        Application.Run(new CalculatorForm());
    }
}
```

### 3. .NET MAUI (Multi-platform App UI)

**Описание**: Современный фреймворк для создания кроссплатформенных приложений.

**Особенности**:
- Единый код для всех платформ
- Поддержка `Android`, `iOS`, `Windows`, `macOS`
- Современный `UI`
- Интеграция с `Blazor`

**Пример MAUI приложения**:
```csharp
// MainPage.xaml
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="MauiApp.MainPage">

    <ScrollView>
        <VerticalStackLayout Spacing="25" Padding="30,0" VerticalOptions="Center">
            
            <Image Source="dotnet_bot.png" 
                   SemanticProperties.Description="Cute dot net bot waving hi to you!"
                   HeightRequest="200"
                   HorizontalOptions="Center" />

            <Label Text="Привет, .NET MAUI!"
                   SemanticProperties.HeadingLevel="Level1"
                   FontSize="32"
                   HorizontalOptions="Center" />

            <Label Text="Сделай шаг в мир кроссплатформенной разработки"
                   SemanticProperties.HeadingLevel="Level2"
                   SemanticProperties.Description="Welcome to dot net Multi platform App UI"
                   FontSize="18"
                   HorizontalOptions="Center" />

            <Button Text="Нажми меня" 
                    x:Name="CounterBtn"
                    SemanticProperties.Hint="Counts the number of times you click"
                    Clicked="OnCounterClicked"
                    HorizontalOptions="Center" />

        </VerticalStackLayout>
    </ScrollView>
</ContentPage>

// MainPage.xaml.cs
namespace MauiApp;

public partial class MainPage : ContentPage
{
    int count = 0;

    public MainPage()
    {
        InitializeComponent();
    }

    private void OnCounterClicked(object sender, EventArgs e)
    {
        count++;

        if (count == 1)
            CounterBtn.Text = $"Нажато {count} раз";
        else
            CounterBtn.Text = $"Нажато {count} раза";

        SemanticScreenReader.Announce(CounterBtn.Text);
    }
}
```

---

## Мобильные фреймворки

### 1. Xamarin (устаревший)

**Описание**: Позволял создавать нативные мобильные приложения для `iOS` и `Android` с использованием `C#`

**Статус**: Заменен `.NET MAUI`

### 2. .NET MAUI

**Уже описан выше** в разделе `Desktop` фреймворков.

### 3. Uno Platform

**Описание**: Позволяет создавать кроссплатформенные приложения с использованием `UWP/XAML`

**Особенности**:
- Использование знакомого `XAML`
- Поддержка `WebAssembly`
- Хорошо подходит для миграции с `WPF/UWP`

---

## ORM и работа с данными

### 1. Entity Framework Core

**Описание**: Современный ORM для .NET.

**Особенности**:
- Code First подход
- LINQ to Entities
- Миграции
- Поддержка множества СУБД

**Установка**:
```bash
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Tools
```

**Пример модели**:
```csharp
using Microsoft.EntityFrameworkCore;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string Description { get; set; } = string.Empty;
}

public class ApplicationDbContext : DbContext
{
    public DbSet<Product> Products { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlServer(
            @"Server=(localdb)\mssqllocaldb;Database=StoreDb;Trusted_Connection=True;");
    }
}
```

**Использование**:
```csharp
using var context = new ApplicationDbContext();

// Добавление данных
var product = new Product 
{ 
    Name = "Ноутбук", 
    Price = 50000, 
    Description = "Мощный ноутбук для работы" 
};
context.Products.Add(product);
context.SaveChanges();

// Получение данных
var products = context.Products.Where(p => p.Price > 10000).ToList();

// Обновление данных
var existingProduct = context.Products.First(p => p.Name == "Ноутбук");
existingProduct.Price = 45000;
context.SaveChanges();

// Удаление данных
context.Products.Remove(existingProduct);
context.SaveChanges();
```

### 2. Dapper

**Описание**: Микро-ORM с высокой производительностью.

**Особенности**:
- Минимальные накладные расходы
- Простота использования
- Подходит для высоконагруженных приложений

**Установка**:
```bash
dotnet add package Dapper
dotnet add package System.Data.SqlClient
```

**Пример использования**:
```csharp
using Dapper;
using System.Data.SqlClient;

public class ProductService
{
    private readonly string _connectionString = 
        @"Server=(localdb)\mssqllocaldb;Database=StoreDb;Trusted_Connection=True;";

    public async Task<IEnumerable<Product>> GetAllProductsAsync()
    {
        using var connection = new SqlConnection(_connectionString);
        return await connection.QueryAsync<Product>(
            "SELECT Id, Name, Price, Description FROM Products");
    }

    public async Task<Product?> GetProductByIdAsync(int id)
    {
        using var connection = new SqlConnection(_connectionString);
        return await connection.QueryFirstOrDefaultAsync<Product>(
            "SELECT Id, Name, Price, Description FROM Products WHERE Id = @Id", 
            new { Id = id });
    }

    public async Task<int> CreateProductAsync(Product product)
    {
        using var connection = new SqlConnection(_connectionString);
        var sql = @"INSERT INTO Products (Name, Price, Description) 
                   VALUES (@Name, @Price, @Description);
                   SELECT CAST(SCOPE_IDENTITY() as int)";
        
        return await connection.QuerySingleAsync<int>(sql, product);
    }
}
```

### 3. NHibernate

**Описание**: Зрелый ORM для .NET, вдохновленный Hibernate для Java.

**Особенности**:
- Мощные возможности маппинга
- Поддержка lazy loading
- Кэширование второго уровня

---

## Тестирование

### 1. xUnit

**Описание**: Популярный фреймворк для модульного тестирования.

**Установка**:
```bash
dotnet add package xunit
dotnet add package xunit.runner.visualstudio
dotnet add package Microsoft.NET.Test.Sdk
```

**Пример теста**:
```csharp
using Xunit;

public class CalculatorTests
{
    [Fact]
    public void Add_TwoNumbers_ReturnsCorrectSum()
    {
        // Arrange
        var calculator = new Calculator();
        
        // Act
        var result = calculator.Add(2, 3);
        
        // Assert
        Assert.Equal(5, result);
    }

    [Theory]
    [InlineData(1, 2, 3)]
    [InlineData(-1, 1, 0)]
    [InlineData(0, 0, 0)]
    public void Add_VariousNumbers_ReturnsCorrectSum(int a, int b, int expected)
    {
        // Arrange
        var calculator = new Calculator();
        
        // Act
        var result = calculator.Add(a, b);
        
        // Assert
        Assert.Equal(expected, result);
    }
}

public class Calculator
{
    public int Add(int a, int b) => a + b;
    public int Subtract(int a, int b) => a - b;
    public int Multiply(int a, int b) => a * b;
    public double Divide(int a, int b)
    {
        if (b == 0) throw new DivideByZeroException();
        return (double)a / b;
    }
}
```

### 2. NUnit

**Описание**: Еще один популярный фреймворк для тестирования.

**Установка**:
```bash
dotnet add package NUnit
dotnet add package NUnit3TestAdapter
dotnet add package Microsoft.NET.Test.Sdk
```

### 3. Moq

**Описание**: Библиотека для создания mock-объектов.

**Установка**:
```bash
dotnet add package Moq
```

**Пример использования**:
```csharp
using Moq;
using Xunit;

public class OrderServiceTests
{
    [Fact]
    public void ProcessOrder_ValidOrder_CallsPaymentService()
    {
        // Arrange
        var mockPaymentService = new Mock<IPaymentService>();
        var orderService = new OrderService(mockPaymentService.Object);
        
        var order = new Order 
        { 
            Id = 1, 
            Amount = 100, 
            CustomerEmail = "test@example.com" 
        };

        // Act
        orderService.ProcessOrder(order);

        // Assert
        mockPaymentService.Verify(
            ps => ps.ProcessPayment(order.Amount, order.CustomerEmail), 
            Times.Once);
    }
}

public interface IPaymentService
{
    bool ProcessPayment(decimal amount, string customerEmail);
}

public class OrderService
{
    private readonly IPaymentService _paymentService;

    public OrderService(IPaymentService paymentService)
    {
        _paymentService = paymentService;
    }

    public void ProcessOrder(Order order)
    {
        // Логика обработки заказа
        var paymentResult = _paymentService.ProcessPayment(order.Amount, order.CustomerEmail);
        
        if (paymentResult)
        {
            // Сохранить заказ
        }
    }
}

public class Order
{
    public int Id { get; set; }
    public decimal Amount { get; set; }
    public string CustomerEmail { get; set; } = string.Empty;
}
```

---

## Утилитарные библиотеки

### 1. Newtonsoft.Json

**Описание**: Популярная библиотека для работы с JSON.

**Установка**:
```bash
dotnet add package Newtonsoft.Json
```

**Пример использования**:
```csharp
using Newtonsoft.Json;

public class Person
{
    public string Name { get; set; } = string.Empty;
    public int Age { get; set; }
    public string Email { get; set; } = string.Empty;
}

// Сериализация
var person = new Person 
{ 
    Name = "Иван Иванов", 
    Age = 30, 
    Email = "ivan@example.com" 
};

string json = JsonConvert.SerializeObject(person, Formatting.Indented);
Console.WriteLine(json);

// Десериализация
string jsonString = @"{
  ""Name"": ""Мария Петрова"",
  ""Age"": 25,
  ""Email"": ""maria@example.com""
}";

Person deserializedPerson = JsonConvert.DeserializeObject<Person>(jsonString);
Console.WriteLine($"Имя: {deserializedPerson.Name}, Возраст: {deserializedPerson.Age}");
```

### 2. AutoMapper

**Описание**: Библиотека для автоматического маппинга объектов.

**Установка**:
```bash
dotnet add package AutoMapper
dotnet add package AutoMapper.Extensions.Microsoft.DependencyInjection
```

**Пример использования**:
```csharp
using AutoMapper;

public class User
{
    public int Id { get; set; }
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public DateTime CreatedDate { get; set; }
}

public class UserDto
{
    public string FullName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string RegistrationInfo { get; set; } = string.Empty;
}

public class MappingProfile : Profile
{
    public MappingProfile()
    {
        CreateMap<User, UserDto>()
            .ForMember(dest => dest.FullName, 
                      opt => opt.MapFrom(src => $"{src.FirstName} {src.LastName}"))
            .ForMember(dest => dest.RegistrationInfo,
                      opt => opt.MapFrom(src => $"Зарегистрирован: {src.CreatedDate:dd.MM.yyyy}"));
    }
}

// Использование
var config = new MapperConfiguration(cfg => cfg.AddProfile<MappingProfile>());
var mapper = config.CreateMapper();

var user = new User
{
    Id = 1,
    FirstName = "Александр",
    LastName = "Смирнов",
    Email = "alex@example.com",
    CreatedDate = DateTime.Now.AddDays(-30)
};

var userDto = mapper.Map<UserDto>(user);
Console.WriteLine($"Полное имя: {userDto.FullName}");
Console.WriteLine($"Email: {userDto.Email}");
Console.WriteLine($"{userDto.RegistrationInfo}");
```

### 3. MediatR

**Описание**: Библиотека для реализации паттерна Mediator.

**Установка**:
```bash
dotnet add package MediatR
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection
```

### 4. FluentValidation

**Описание**: Библиотека для валидации объектов.

**Установка**:
```bash
dotnet add package FluentValidation
```

**Пример использования**:
```csharp
using FluentValidation;

public class Customer
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public int Age { get; set; }
}

public class CustomerValidator : AbstractValidator<Customer>
{
    public CustomerValidator()
    {
        RuleFor(customer => customer.Name)
            .NotEmpty().WithMessage("Имя обязательно")
            .MaximumLength(100).WithMessage("Имя не должно превышать 100 символов");

        RuleFor(customer => customer.Email)
            .NotEmpty().WithMessage("Email обязателен")
            .EmailAddress().WithMessage("Некорректный формат email");

        RuleFor(customer => customer.Age)
            .InclusiveBetween(18, 120).WithMessage("Возраст должен быть от 18 до 120 лет");
    }
}

// Использование
var validator = new CustomerValidator();
var customer = new Customer 
{ 
    Name = "", 
    Email = "invalid-email", 
    Age = 15 
};

var validationResult = validator.Validate(customer);

if (!validationResult.IsValid)
{
    foreach (var error in validationResult.Errors)
    {
        Console.WriteLine($"{error.PropertyName}: {error.ErrorMessage}");
    }
}
```

---

## Выбор подходящего фреймворка

### Таблица сравнения фреймворков

| Фреймворк | Тип | Платформы | Сложность | Производительность | Сообщество |
|-----------|-----|-----------|-----------|-------------------|------------|
| ASP.NET Core | Web | Все | Средняя | Высокая | Большое |
| Blazor | Web | Все | Средняя | Средняя | Среднее |
| WPF | Desktop | Windows | Средняя | Высокая | Большое |
| WinForms | Desktop | Windows | Низкая | Высокая | Большое |
| .NET MAUI | Mobile/Desktop | Все | Средняя | Средняя | Растущее |
| Entity Framework | ORM | Все | Средняя | Средняя | Большое |
| Dapper | ORM | Все | Низкая | Очень высокая | Большое |

### Рекомендации по выбору:

1. **Веб-приложения**:
   - ASP.NET Core (общие веб-приложения)
   - Blazor (SPA, если нужен C# вместо JS)

2. **Десктопные приложения**:
   - WPF (современные, богатые UI)
   - WinForms (простые, быстрые в разработке)
   - .NET MAUI (кроссплатформенные)

3. **Мобильные приложения**:
   - .NET MAUI (единый код для всех платформ)

4. **Работа с данными**:
   - Entity Framework (сложные доменные модели)
   - Dapper (высокая производительность)

---

## Практические примеры

### 1. Веб-API с Entity Framework

```csharp
// Program.cs
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Добавление сервисов
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Middleware
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();

// Models/Product.cs
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string Description { get; set; } = string.Empty;
    public DateTime CreatedDate { get; set; } = DateTime.UtcNow;
}

// Data/ApplicationDbContext.cs
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) { }
    
    public DbSet<Product> Products { get; set; }
}

// Controllers/ProductsController.cs
[ApiController]
[Route("[controller]")]
public class ProductsController : ControllerBase
{
    private readonly ApplicationDbContext _context;

    public ProductsController(ApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<Product>>> GetProducts()
    {
        return await _context.Products.ToListAsync();
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<Product>> GetProduct(int id)
    {
        var product = await _context.Products.FindAsync(id);
        
        if (product == null)
        {
            return NotFound();
        }

        return product;
    }

    [HttpPost]
    public async Task<ActionResult<Product>> PostProduct(Product product)
    {
        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        return CreatedAtAction(nameof(GetProduct), new { id = product.Id }, product);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> PutProduct(int id, Product product)
    {
        if (id != product.Id)
        {
            return BadRequest();
        }

        _context.Entry(product).State = EntityState.Modified;

        try
        {
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateConcurrencyException)
        {
            if (!ProductExists(id))
            {
                return NotFound();
            }
            else
            {
                throw;
            }
        }

        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteProduct(int id)
    {
        var product = await _context.Products.FindAsync(id);
        if (product == null)
        {
            return NotFound();
        }

        _context.Products.Remove(product);
        await _context.SaveChangesAsync();

        return NoContent();
    }

    private bool ProductExists(int id)
    {
        return _context.Products.Any(e => e.Id == id);
    }
}
```

### 2. WPF MVVM приложение

```csharp
// ViewModel/MainWindowViewModel.cs
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;

public class MainWindowViewModel : INotifyPropertyChanged
{
    private string _firstName = "";
    private string _lastName = "";
    private string _fullName = "";

    public string FirstName
    {
        get => _firstName;
        set
        {
            _firstName = value;
            OnPropertyChanged();
            UpdateFullName();
        }
    }

    public string LastName
    {
        get => _lastName;
        set
        {
            _lastName = value;
            OnPropertyChanged();
            UpdateFullName();
        }
    }

    public string FullName
    {
        get => _fullName;
        set
        {
            _fullName = value;
            OnPropertyChanged();
        }
    }

    public ICommand ClearCommand { get; }

    public MainWindowViewModel()
    {
        ClearCommand = new RelayCommand(ClearFields);
    }

    private void UpdateFullName()
    {
        FullName = $"{FirstName} {LastName}".Trim();
    }

    private void ClearFields()
    {
        FirstName = "";
        LastName = "";
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    protected virtual void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}

// Commands/RelayCommand.cs
using System;
using System.Windows.Input;

public class RelayCommand : ICommand
{
    private readonly Action _execute;
    private readonly Func<bool>? _canExecute;

    public RelayCommand(Action execute, Func<bool>? canExecute = null)
    {
        _execute = execute ?? throw new ArgumentNullException(nameof(execute));
        _canExecute = canExecute;
    }

    public event EventHandler? CanExecuteChanged
    {
        add { CommandManager.RequerySuggested += value; }
        remove { CommandManager.RequerySuggested -= value; }
    }

    public bool CanExecute(object? parameter) => _canExecute?.Invoke() ?? true;

    public void Execute(object? parameter) => _execute();
}

// MainWindow.xaml
<Window x:Class="WpfMvvmApp.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="MVVM Пример" Height="300" Width="400">
    <Grid Margin="20">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
        </Grid.RowDefinitions>
        
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="Auto"/>
            <ColumnDefinition Width="*"/>
        </Grid.ColumnDefinitions>
        
        <Label Grid.Row="0" Grid.Column="0" Content="Имя:" VerticalAlignment="Center"/>
        <TextBox Grid.Row="0" Grid.Column="1" Text="{Binding FirstName, UpdateSourceTrigger=PropertyChanged}" 
                 Margin="5"/>
        
        <Label Grid.Row="1" Grid.Column="0" Content="Фамилия:" VerticalAlignment="Center"/>
        <TextBox Grid.Row="1" Grid.Column="1" Text="{Binding LastName, UpdateSourceTrigger=PropertyChanged}" 
                 Margin="5"/>
        
        <Label Grid.Row="2" Grid.Column="0" Content="Полное имя:" VerticalAlignment="Center"/>
        <TextBox Grid.Row="2" Grid.Column="1" Text="{Binding FullName}" 
                 Margin="5" IsReadOnly="True"/>
        
        <Button Grid.Row="3" Grid.Column="0" Grid.ColumnSpan="2" 
                Content="Очистить" Command="{Binding ClearCommand}" 
                Margin="5" Padding="10,5"/>
    </Grid>
</Window>

// App.xaml.cs
public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);
        
        var viewModel = new MainWindowViewModel();
        var mainWindow = new MainWindow
        {
            DataContext = viewModel
        };
        mainWindow.Show();
    }
}
```

---

## Заключение

C# и .NET экосистема предлагает богатый выбор фреймворков для различных задач разработки. Выбор правильного фреймворка зависит от требований проекта, целевой платформы и предпочтений разработчика.

### Ключевые рекомендации:
1. **Изучите документацию** выбранного фреймворка
2. **Начинайте с простых примеров**
3. **Используйте NuGet** для управления пакетами
4. **Следите за обновлениями** .NET
5. **Участвуйте в сообществах** разработчиков

### Полезные ресурсы:
- [Microsoft Learn](https://learn.microsoft.com/ru-ru/)
- [NuGet Gallery](https://www.nuget.org/)
- [.NET Foundation](https://dotnetfoundation.org/)
- [GitHub .NET](https://github.com/dotnet)

Это руководство охватывает основные фреймворки и библиотеки `C#`

Для углубленного изучения каждого инструмента рекомендуется обращаться к официальной документации и примерам кода.

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