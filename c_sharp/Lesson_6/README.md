# Урок 6: Обработка строк в C#

**Цель урока:** Научиться выполнять основные операции со строками, конкатенировать и форматировать их, а также познакомиться с основами регулярных выражений.

### 1. Основные операции со строками

**Строки** — это последовательности символов, доступные для различных операций:

**Пример:**

```csharp
string name = "Maestro";
Console.WriteLine(name.Length); // Длина строки
Console.WriteLine(name.ToUpper()); // Преобразование в верхний регистр
```

### 2. Конкатенация и форматирование строк

**Конкатенация:**

```csharp
string firstName = "John";
string lastName = "Doe";
string fullName = firstName + " " + lastName;
Console.WriteLine(fullName); // John Doe
```

**Форматирование с использованием интерполяции:**

```csharp
int age = 25;
string message = $"Возраст: {age}";
Console.WriteLine(message); // Возраст: 25
```

### 3. Введение в регулярные выражения

Регулярные выражения используются для поиска и работы с шаблонами в строках.

**Пример:**

```csharp
using System.Text.RegularExpressions;

string pattern = @"\d+";
string input = "В комнате 15 человек";
Match match = Regex.Match(input, pattern);
Console.WriteLine(match.Value); // 15
```



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**