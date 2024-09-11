# Объектно-ориентированное программирование (ООП) на C#

Давайте разберём ключевые концепции объектно-ориентированного программирования (ООП) на C#.

**Классы и объекты**

**Класс в C#** — это шаблон для создания объектов.

Он определяет состояние (поля) и поведение (методы) объектов, которые будут созданы на основе этого класса.

**Пример класса:**

```csharp
public class Car
{
    // Поля (состояние)
    public string Brand;
    public string Model;
    public int Year;

    // Метод (поведение)
    public void Start()
    {
        Console.WriteLine("Car started");
    }
}
```

**Объект** — это экземпляр класса.

Объекты создаются с помощью оператора `new`.

**Пример создания объекта:**

```csharp
Car myCar = new Car();
myCar.Brand = "Toyota";
myCar.Model = "Camry";
myCar.Year = 2020;
myCar.Start();
```

Инкапсуляция, наследование и полиморфизм
========================================
**Инкапсуляция** — это механизм скрытия внутренней реализации объекта от внешнего мира и предоставление доступа к данным и методам через публичные интерфейсы.

**Пример инкапсуляции:**

```csharp
public class Person
{
    private string name;
    private int age;

    public void SetName(string newName)
    {
        name = newName;
    }

    public string GetName()
    {
        return name;
    }

    public void SetAge(int newAge)
    {
        if (newAge > 0)
        {
            age = newAge;
        }
    }

    public int GetAge()
    {
        return age;
    }
}
```

Наследование позволяет создать новый класс на основе уже существующего.

Новый класс наследует свойства и методы от базового класса и может добавлять собственные.

**Пример наследования:**

```csharp
public class Animal
{
    public void Eat()
    {
        Console.WriteLine("Animal is eating");
    }
}

public class Dog : Animal
{
    public void Bark()
    {
        Console.WriteLine("Dog is barking");
    }
}
```

**Полиморфизм** — это способность объектов разных классов обрабатывать вызовы методов через единый интерфейс.

Полиморфизм достигается через переопределение методов и использование интерфейсов.

**Пример полиморфизма:**

```csharp
public class Animal
{
    public virtual void MakeSound()
    {
        Console.WriteLine("Animal makes a sound");
    }
}

public class Dog : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine("Dog barks");
    }
}

public class Cat : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine("Cat meows");
    }
}

public class Program
{
    public static void Main()
    {
        Animal myAnimal = new Dog();
        myAnimal.MakeSound(); // Выведет: Dog barks

        myAnimal = new Cat();
        myAnimal.MakeSound(); // Выведет: Cat meows
    }
}
```

**Конструкторы и деструкторы**

**Конструктор** — это специальный метод, который вызывается при создании объекта.

Он используется для инициализации объекта.

**Пример конструктора:**

```csharp
public class Book
{
    public string Title;
    public string Author;

    // Конструктор
    public Book(string title, string author)
    {
        Title = title;
        Author = author;
    }
}
```

**Деструктор** — это метод, который вызывается при удалении объекта.

Он используется для освобождения ресурсов.

**Пример деструктора:**

```csharp
public class Resource
{
    // Деструктор
    ~Resource()
    {
        Console.WriteLine("Resource is being deleted");
    }
}
```



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**