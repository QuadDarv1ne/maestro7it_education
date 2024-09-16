# Работа с файлами в C#

Работа с файлами в C# включает чтение и запись данных, а также управление потоками ввода/вывода. Рассмотрим основные операции и методы.

### Чтение и запись файлов

### Чтение и запись текстовых файлов

#### Чтение текстового файла

```csharp
using System;
using System.IO;

public class Program
{
    public static void Main()
    {
        // Чтение всего содержимого файла
        string content = File.ReadAllText("example.txt");
        Console.WriteLine(content);

        // Чтение файла построчно
        string[] lines = File.ReadAllLines("example.txt");
        foreach (string line in lines)
        {
            Console.WriteLine(line);
        }
    }
}
```

#### Запись в текстовый файл

```csharp
Копировать код
using System;
using System.IO;

public class Program
{
    public static void Main()
    {
        string[] lines = { "Line 1", "Line 2", "Line 3" };

        // Запись массива строк в файл
        File.WriteAllLines("example.txt", lines);

        // Запись текста в файл
        File.WriteAllText("example.txt", "Hello, World!");
    }
}
```

### Чтение и запись бинарных файлов

#### Чтение бинарного файла

```csharp
using System;
using System.IO;

public class Program
{
    public static void Main()
    {
        byte[] data = File.ReadAllBytes("example.bin");
        Console.WriteLine("Чтение бинарных данных:");
        foreach (byte b in data)
        {
            Console.Write($"{b:X2} ");
        }
    }
}
```

#### Запись в бинарный файл

```csharp
using System;
using System.IO;

public class Program
{
    public static void Main()
    {
        byte[] data = { 0x01, 0x02, 0x03, 0x04 };
        File.WriteAllBytes("example.bin", data);
    }
}
```

### Потоковый ввод/вывод

Потоки ввода/вывода позволяют работать с данными по частям, что удобно при работе с большими файлами или при необходимости выполнения более сложных операций.

#### Использование FileStream для чтения и записи

```csharp
using System;
using System.IO;

public class Program
{
    public static void Main()
    {
        // Запись данных в файл
        using (FileStream fs = new FileStream("example.bin", FileMode.Create))
        {
            byte[] data = { 0x01, 0x02, 0x03, 0x04 };
            fs.Write(data, 0, data.Length);
        }

        // Чтение данных из файла
        using (FileStream fs = new FileStream("example.bin", FileMode.Open))
        {
            byte[] data = new byte[fs.Length];
            fs.Read(data, 0, data.Length);
            Console.WriteLine("Чтение данных из файла:");
            foreach (byte b in data)
            {
                Console.Write($"{b:X2} ");
            }
        }
    }
}
```

#### Использование StreamReader и StreamWriter для работы с текстовыми файлами

```csharp
using System;
using System.IO;

public class Program
{
    public static void Main()
    {
        // Запись текста в файл
        using (StreamWriter sw = new StreamWriter("example.txt"))
        {
            sw.WriteLine("Hello, World!");
            sw.WriteLine("This is a new line.");
        }

        // Чтение текста из файла
        using (StreamReader sr = new StreamReader("example.txt"))
        {
            string line;
            while ((line = sr.ReadLine()) != null)
            {
                Console.WriteLine(line);
            }
        }
    }
}
```

### Примеры использования потоков и файлов

#### Создание и запись в файл с использованием потоков

```csharp
using System;
using System.IO;

public class Program
{
    public static void Main()
    {
        string path = "example.txt";

        using (FileStream fs = new FileStream(path, FileMode.Create))
        using (StreamWriter sw = new StreamWriter(fs))
        {
            sw.WriteLine("Hello, FileStream!");
        }
    }
}
```

#### Чтение и запись данных в поток

```csharp
using System;
using System.IO;

public class Program
{
    public static void Main()
    {
        string path = "example.txt";
        string content = "Hello, StreamReader and StreamWriter!";

        // Запись данных в поток
        using (FileStream fs = new FileStream(path, FileMode.Create))
        using (StreamWriter sw = new StreamWriter(fs))
        {
            sw.Write(content);
        }

        // Чтение данных из потока
        using (FileStream fs = new FileStream(path, FileMode.Open))
        using (StreamReader sr = new StreamReader(fs))
        {
            string readContent = sr.ReadToEnd();
            Console.WriteLine("Содержимое файла:");
            Console.WriteLine(readContent);
        }
    }
}
```



**Автор:** Дуплей Максим Игоревич

**Дата:** 11.09.2024

**Версия:** 1.0