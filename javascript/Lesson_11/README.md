# Модули и современный JavaScript (ES6+)

Современный `JavaScript (ES6+)` включает множество нововведений, которые упрощают разработку и улучшают читаемость кода.

Вот основные особенности и методы работы с модулями, деструктуризацией, стрелочными функциями и шаблонными строками.

### Импорт и Экспорт Модулей

Модули в JavaScript позволяют разбивать код на отдельные части, которые могут быть импортированы и экспортированы.

Это помогает организовать код и улучшить его структуру.

#### 1. Экспорт

- **Экспорт по умолчанию:** Экспорт одного значения или функции по умолчанию из модуля.

```javascript
// math.js
export default function add(a, b) {
  return a + b;
}
```

- **Именованный экспорт:** Экспорт нескольких значений или функций из модуля.

```javascript
// math.js
export function add(a, b) {
  return a + b;
}

export function subtract(a, b) {
  return a - b;
}
```

#### 2. Импорт

- **Импорт по умолчанию:** Импорт значения или функции по умолчанию из модуля.

```javascript
// app.js
import add from './math.js';
console.log(add(2, 3)); // 5
```

- **Именованный импорт:** Импорт конкретных значений или функций из модуля.

```javascript
// app.js
import { add, subtract } from './math.js';
console.log(add(2, 3)); // 5
console.log(subtract(5, 2)); // 3
```

- **Импорт всего модуля:** Импорт всего модуля как объекта.

```javascript
// app.js
import * as math from './math.js';
console.log(math.add(2, 3)); // 5
console.log(math.subtract(5, 2)); // 3
```

### Деструктуризация, Стрелочные Функции и Шаблонные Строки

#### 1. Деструктуризация

Деструктуризация позволяет извлекать данные из массивов и объектов в отдельные переменные.

- Деструктуризация массива

```javascript
const numbers = [1, 2, 3];
const [one, two, three] = numbers;
console.log(one); // 1
console.log(two); // 2
console.log(three); // 3
```

- Деструктуризация объекта

```javascript
const person = { name: 'John', age: 30 };
const { name, age } = person;
console.log(name); // John
console.log(age); // 30
```

- Деструктуризация с значениями по умолчанию

```javascript
const person = { name: 'John' };
const { name, age = 25 } = person;
console.log(name); // John
console.log(age); // 25
```

### 2. Стрелочные функции

Стрелочные функции (=>) предлагают более краткий синтаксис для объявления функций и не имеют собственного `this`.

- Пример базовой стрелочной функции

```javascript
const add = (a, b) => a + b;
console.log(add(2, 3)); // 5
```

- Стрелочные функции с одним параметром

```javascript
const square = x => x * x;
console.log(square(4)); // 16
```

- Стрелочные функции без параметров

```javascript
const greet = () => 'Hello, world!';
console.log(greet()); // Hello, world!
```

- Стрелочные функции с многострочным телом

```javascript
const add = (a, b) => {
  const result = a + b;
  return result;
};
console.log(add(2, 3)); // 5
```

### 3. Шаблонные строки

Шаблонные строки (или шаблонные литералы) позволяют создавать строки с интерполяцией выражений и многострочные строки.

- Пример интерполяции выражений

```javascript
const name = 'John';
const age = 30;
const greeting = `Hello, my name is ${name} and I am ${age} years old.`;
console.log(greeting); // Hello, my name is John and I am 30 years old.
```

- Многострочные строки

```javascript
const multiLineString = `
  This is a string
  that spans multiple lines.
`;
console.log(multiLineString);
```

### Нововведения в ES6+

#### 1. `let` и `const`

- `let`: Позволяет объявить переменные с блочной областью видимости.

```javascript
let x = 10;
if (true) {
  let x = 20;
  console.log(x); // 20
}
console.log(x); // 10
```

- `const`: Позволяет объявить константы, которые не могут быть переназначены.

```javascript
const PI = 3.14;
PI = 3.14159; // Ошибка
```

#### 2. Классы

ES6 добавил синтаксис классов, который делает создание объектов и работу с наследованием проще и более понятной.

```javascript
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }

  greet() {
    return `Hello, my name is ${this.name}`;
  }
}

const john = new Person('John', 30);
console.log(john.greet()); // Hello, my name is John
```

#### 3. Модули

Как уже упоминалось, модули позволяют организовывать код в независимые части, которые могут быть импортированы и экспортированы.

#### 4. Синтаксис асинхронных функций `async/await`

Асинхронные функции позволяют писать асинхронный код более читаемым и понятным способом.

```javascript
async function fetchData() {
  try {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error:', error);
  }
}

fetchData();
```

Эти возможности и улучшения делают современный JavaScript более мощным и удобным для разработки сложных веб-приложений.

---

**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
