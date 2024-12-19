# Введение в Node.js: Серверная часть JavaScript

**Node.js** — это серверная платформа, основанная на движке `V8 от Google Chrome`, которая позволяет запускать JavaScript вне браузера.

Это делает JavaScript полноценным языком для серверной разработки, помимо его традиционного использования в браузере.

### Основы Node.js

#### 1. Установка и Настройка

Для начала работы с `Node.js` необходимо его установить.

Скачайте последнюю версию с официального сайта Node.js и следуйте инструкциям по установке.

**После установки Node.js можно проверить его версию и установить `npm (Node Package Manager)`, который идет в комплекте:**

```bash
node -v
npm -v
```

#### 2. Основы работы с Node.js

`Hello World на Node.js`

**Создайте файл `app.js` с простым сервером:**

```javascript
// app.js
const http = require('http');

// Создаем HTTP сервер
const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World\n');
});

// Запускаем сервер
const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
});
```

**Запустите сервер командой:**

```bash
node app.js
```

Откройте в браузере `http://localhost:3000`, и вы увидите сообщение `Hello World`

#### 3. Модули и Пакеты

`Node.js` использует модульную систему для организации кода.

Модули можно импортировать и экспортировать с помощью `require` и `module.exports`.

**Создание и использование модуля**

**Модуль `math.js`:**

```javascript
// math.js
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

module.exports = { add, subtract };
```

**Использование модуля в `app.js`:**

```
// app.js
const math = require('./math');

console.log(math.add(2, 3)); // 5
console.log(math.subtract(5, 2)); // 3
```

#### 4. Асинхронное Программирование

`Node.js` активно использует асинхронное программирование, что позволяет эффективно обрабатывать множество одновременных запросов.

**Пример асинхронной функции с использованием `setTimeout`:**

```javascript
console.log('Start');

setTimeout(() => {
  console.log('This message is shown after 2 seconds');
}, 2000);

console.log('End');
```

**Вывод будет следующим:**

```
Start
End
This message is shown after 2 seconds
```

**Использование промисов и `async/await`:**

```
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function asyncFunction() {
  console.log('Start');
  await delay(2000);
  console.log('This message is shown after 2 seconds');
  console.log('End');
}

asyncFunction();
```

#### 5. Работа с Файловой Системой

`Node.js` предоставляет модуль `fs` для работы с файловой системой.

**Пример чтения файла:**

```javascript
const fs = require('fs');

// Чтение файла асинхронно
fs.readFile('example.txt', 'utf8', (err, data) => {
  if (err) throw err;
  console.log(data);
});
```

**Пример записи в файл:**

```javascript
const fs = require('fs');

// Запись в файл
fs.writeFile('example.txt', 'Hello Node.js!', err => {
  if (err) throw err;
  console.log('File has been saved!');
});
```

#### 6. Использование `Express.js`

`Express.js` — это популярный фреймворк для Node.js, упрощающий создание веб-серверов и маршрутизацию.

**Установка Express:**

```bash
npm install express
```

**Пример создания сервера с использованием `Express.js`:**

```javascript
const express = require('express');
const app = express();

// Маршрут для корневого адреса
app.get('/', (req, res) => {
  res.send('Hello World');
});

// Запуск сервера
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
});
```

#### 7. Управление Пакетами и Зависимостями

**Создание `package.json`**

Файл `package.json` хранит метаданные вашего проекта и зависимости.

**Создайте его с помощью:**

```bash
npm init
```

**Установка зависимостей**

Зависимости устанавливаются с помощью `npm install`.

**Например, установка `express`:**

```bash
npm install express
```

**Удаление зависимостей**

```bash
npm uninstall express
```

---

### Выводы

`Node.js` предоставляет мощные возможности для серверной разработки с использованием `JavaScript`

С помощью его асинхронных возможностей, модульной системы и фреймворков, таких как `Express.js`, вы можете легко создавать масштабируемые серверные приложения.

Node.js активно используется в индустрии благодаря своей производительности и гибкости.

---

**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
