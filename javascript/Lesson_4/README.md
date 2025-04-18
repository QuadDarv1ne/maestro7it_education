# Условные операторы и циклы в JavaScript

## 1. Условные операторы

Условные операторы используются для выполнения различных блоков кода в зависимости от условий.

### if...else
```javascript
let number = 10;

if (number > 0) {
  console.log("Число положительное");
} else if (number === 0) {
  console.log("Число равно нулю");
} else {
  console.log("Число отрицательное");
}
```
- **if**: Выполняет блок кода, если условие истинно.
- **else if**: Добавляет дополнительные условия.
- **else**: Выполняется, если все условия ложны.

### switch
```javascript
let color = "red";

switch (color) {
  case "red":
    console.log("Вы выбрали красный");
    break;
  case "blue":
    console.log("Вы выбрали синий");
    break;
  default:
    console.log("Цвет не распознан");
}
```
- **case**: Определяет варианты для сравнения.
- **break**: Завершает выполнение текущего блока.
- **default**: Выполняется, если ни одно из условий не подошло.

---

## 2. Циклы

Циклы позволяют многократно выполнять один и тот же блок кода.

### for
```javascript
for (let i = 1; i <= 5; i++) {
  console.log(`Итерация: ${i}`);
}
```
Используется, когда заранее известно количество итераций.

### while
```javascript
let count = 0;

while (count < 3) {
  console.log(`Счётчик: ${count}`);
  count++;
}
```
Выполняет код, пока условие истинно.

### do...while
```javascript
let num = 0;

do {
  console.log(`Число: ${num}`);
  num++;
} while (num < 3);
```
Сначала выполняет код, затем проверяет условие.

---

## 3. Управляющие операторы

Управляющие операторы позволяют изменять выполнение цикла.

### break
```javascript
for (let i = 1; i <= 5; i++) {
  if (i === 3) {
    break; // Прерывает цикл на третьей итерации
  }
  console.log(i);
}
```
Прерывает выполнение текущего цикла.

### continue
```javascript
for (let i = 1; i <= 5; i++) {
  if (i === 3) {
    continue; // Пропускает третью итерацию
  }
  console.log(i);
}
```
Пропускает текущую итерацию и переходит к следующей.

---

## Примечания

- Используйте **if...else** для проверки нескольких условий.
- **switch** удобен для проверки одного значения на равенство.
- Избегайте чрезмерного использования **break** и **continue**, чтобы не усложнять код.

---

# Функции в JavaScript

## 4. Функции: объявление и вызов

Функции позволяют структурировать код и выполнять повторяющиеся операции.

### Определение функций
```javascript
function greet(name) {
  console.log(`Привет, ${name}!`);
}

greet("Мир"); // Вызов функции
```
- **function**: Ключевое слово для объявления функции.
- **name**: Параметр функции.
- **greet("Мир")**: Вызов функции с аргументом "Мир".

### Аргументы функций и возвращаемые значения
```javascript
function add(a, b) {
  return a + b; // Возвращает сумму аргументов
}

let result = add(5, 3);
console.log(result); // 8
```
- **a, b**: Аргументы функции.
- **return**: Возвращает значение из функции.

### Замыкания и контексты функций
```javascript
function makeCounter() {
  let count = 0;

  return function () {
    count++;
    return count;
  };
}

let counter = makeCounter();
console.log(counter()); // 1
console.log(counter()); // 2
```
- **Замыкание**: Функция, которая запоминает своё окружение.
- **count**: Переменная остаётся доступной для вложенной функции.

---

**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
