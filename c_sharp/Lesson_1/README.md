# Урок 1: Введение в C#: Установка и настройка среды разработки

**Цели урока:**

- Познакомиться с языком программирования C# и его применением.
- Установить и настроить необходимое программное обеспечение.
- Написать и запустить первую программу на C#.

### 1. Введение в C#

**C# (произносится как "си-шарп")** — это объектно-ориентированный язык программирования, разработанный корпорацией Microsoft.

Он является мощным и универсальным инструментом, который используется для разработки различных приложений: от десктопных программ до веб-сервисов и игр.

### 2. Установка .NET SDK

Для работы с C# нам необходимо установить **.NET SDK** — платформу, на которой работает C#.
Перейдите на [официальный сайт .NET](https://dotnet.microsoft.com/ru-ru/) и [скачайте последнюю версию SDK](https://dotnet.microsoft.com/ru-ru/download) для вашей операционной системы.

### 3. Установка IDE

Для разработки на C# удобнее всего использовать интегрированную среду разработки (IDE).

**Мы будем использовать Visual Studio или Visual Studio Code:**

- `Visual Studio` — это мощная IDE от Microsoft с поддержкой всех возможностей C#.
- `Visual Studio Code` — легковесный редактор, который можно настроить для работы с C# через расширения.

Установите одну из этих сред разработки и настройте ее для работы с C#.

### 4. Первая программа на C#

Откройте Visual Studio или Visual Studio Code.

Создайте новый проект, выбрав тип проекта `"Консольное приложение"` (Console App).

**В файле `Program.cs` вы увидите код по умолчанию:**

```csharp
using System;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, Worl!");
    }
}
```
Нажмите кнопку `"Запустить"` (или используйте команду dotnet run в терминале), чтобы выполнить программу. В консоли появится сообщение: `Hello, World`

### 5. Разбор программы

- `using System;` — эта строка подключает библиотеку System, которая содержит основные функции, такие как работа с консолью.
- `class Program` — определение класса. В C# весь код должен быть внутри классов.
- `static void Main(string[] args)` — это точка входа в программу. Именно с этого метода начинается выполнение.
- `Console.WriteLine("Hello, World");` — команда, которая выводит текст в консоль.

### 6. Заключение

На этом уроке мы познакомились с языком C#, установили и настроили среду разработки, а также написали и запустили первую программу.

В следующих уроках мы начнем разбирать синтаксис языка и углубляться в его возможности.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**