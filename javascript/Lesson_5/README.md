# Массивы и объекты в JavaScript

В этом разделе рассматриваются основные концепции и методы работы с массивами и объектами в языке JavaScript.

## 1. Массивы

`Массивы` — это упорядоченные коллекции данных.

Они могут содержать элементы различных типов и поддерживают индексацию.

### 1.1 Создание массива

**Массив можно создать несколькими способами:**

```javascript
// Литерал массива
let fruits = ['apple', 'banana', 'cherry'];

// Конструктор массива
let numbers = new Array(1, 2, 3, 4);
```

### 1.2 Доступ к элементам массива

**Для получения элемента массива используйте индекс:**

```javascript
let firstFruit = fruits[0]; // 'apple'
let secondNumber = numbers[1]; // 2
```

### 1.3 Встроенные методы для работы с массивами

**`JavaScript` предоставляет множество встроенных методов для работы с массивами:**

- `push()`: Добавляет элементы в конец массива
- `pop()`: Удаляет последний элемент массива
- `shift()`: Удаляет первый элемент массива
- `unshift()`: Добавляет элементы в начало массива
- `map()`: Создает новый массив с результатами выполнения функции для каждого элемента
- `filter()`: Создает новый массив с элементами, которые удовлетворяют условию
- `forEach()`: Выполняет функцию для каждого элемента массива

**Примеры:**

```javascript
fruits.push('orange'); // Добавляет 'orange' в конец
fruits.pop(); // Удаляет последний элемент массива

let doubledNumbers = numbers.map(num => num * 2); // [2, 4, 6, 8]
let evenNumbers = numbers.filter(num => num % 2 === 0); // [2, 4]
```

## 2. Объекты

`Объекты в JavaScript` — это коллекции данных в виде пар "ключ-значение".

### 2.1 Создание объекта

**Объект можно создать с помощью литерала объекта:**

```javascript
let person = {
    name: 'John',
    age: 30,
    greet: function() {
        return 'Привет, меня зовут ' + this.name;
    }
};
```

### 2.2 Доступ к значениям объекта

**Для доступа к значениям объекта используйте ключи:**

```javascript
let personName = person.name; // 'John'
let personGreeting = person.greet(); // 'Привет, меня зовут John'
```

### 2.3 Встроенные методы для работы с объектами

- `Object.keys()`: Возвращает массив всех ключей объекта
- `Object.values()`: Возвращает массив всех значений объекта
- `Object.entries()`: Возвращает массив всех пар ключ-значение

**Примеры:**

```javascript
let keys = Object.keys(person); // ['name', 'age', 'greet']
let values = Object.values(person); // ['John', 30, function() {...}]
```

```java
import java.util.Arrays;      // Импорт для Arrays.toString()
import java.util.ArrayList;   // Импорт для ArrayList
import java.util.List;        // Импорт для интерфейса List

public class ArrayDemo {
    public static void main(String[] args) {
        // 1. Литерал массива
        String[] fruits = {"apple", "banana", "cherry"};
        System.out.println("Фрукты: " + Arrays.toString(fruits));
        
        // 2. Через new с инициализацией
        int[] numbers = new int[]{1, 2, 3, 4};
        System.out.println("Числа: " + Arrays.toString(numbers));
        
        // 3. Создание пустого массива
        double[] prices = new double[3];
        prices[0] = 12.5;
        prices[1] = 7.99;
        prices[2] = 3.49;
        System.out.println("Цены: " + Arrays.toString(prices));
        
        // 4. Многомерный массив
        int[][] matrix = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        System.out.println("Матрица 3x3:");
        for (int[] row : matrix) {
            System.out.println(Arrays.toString(row));
        }
        
        // 5. ArrayList (динамический массив)
        List<String> fruitList = new ArrayList<>();
        fruitList.add("apple");
        fruitList.add("banana");
        fruitList.add("cherry");
        System.out.println("ArrayList: " + fruitList);
        
        // Удаление элемента (в обычном массиве невозможно)
        fruitList.remove("cherry");
        System.out.println("После удаления: " + fruitList);
    }
}
```

---

**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
