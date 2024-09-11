# Урок 5: Массивы и коллекции в C#

**Цель урока:** Изучить работу с массивами и коллекциями, их типы и способы итерации.

### 1. Одномерные и многомерные массивы

**Массивы** — это структуры данных, хранящие элементы одного типа.

**Одномерный массив:**

```csharp
int[] numbers = { 1, 2, 3, 4, 5 };
Console.WriteLine(numbers[0]); // Вывод: 1
```

**Многомерный массив:**

```csharp
int[,] matrix = { { 1, 2 }, { 3, 4 } };
Console.WriteLine(matrix[0, 1]); // Вывод: 2
```

### 2. Коллекции: списки, словари, очереди и стеки

**Список (List<T>):**

Динамическая коллекция, которая изменяет размер в зависимости от количества элементов.

**Пример:**

```csharp
List<int> list = new List<int> { 1, 2, 3 };
list.Add(4);
```

**Словарь (Dictionary<TKey, TValue>):**

`Коллекция пар "ключ-значение"`.

**Пример:**

```csharp
Dictionary<string, int> dict = new Dictionary<string, int>();
dict.Add("apple", 5);
Console.WriteLine(dict["apple"]); // Вывод: 5
```

**Очередь (Queue<T>):**

Работает по принципу `FIFO (первый вошел — первый вышел)`.

**Пример:**

```csharp
Queue<string> queue = new Queue<string>();
queue.Enqueue("first");
queue.Enqueue("second");
Console.WriteLine(queue.Dequeue()); // Вывод: first
```

**Стек (Stack<T>):**

Работает по принципу `LIFO (последний вошел — первый вышел)`.

**Пример:**

```csharp
Stack<string> stack = new Stack<string>();
stack.Push("bottom");
stack.Push("top");
Console.WriteLine(stack.Pop()); // Вывод: top
```

### 3. Работа с коллекциями и их итерация

Итерация по коллекциям возможна с помощью циклов, таких как `for`, `foreach`.

**Пример с foreach:**

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };
foreach (int num in numbers)
{
    Console.WriteLine(num);
}
```



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**