# Работа с веб-API: AJAX и Fetch

![Работа с веб-API: AJAX и Fetch](https://github.com/user-attachments/assets/7d702894-e17e-457a-835e-b107c2ba608e)

Работа с веб-API в JavaScript позволяет взаимодействовать с внешними сервисами и получать или отправлять данные на сервер.

**В JavaScript для этого можно использовать два основных подхода:** `XMLHttpRequest` и `fetch`.

**Вот как можно работать с API, используя эти технологии:**

### Основы Работы с API

Веб-API предоставляет интерфейсы для взаимодействия с различными сервисами через HTTP-запросы.

**Основные операции, которые можно выполнять с API, включают:**

- **`GET-запросы`**: Получение данных с сервера.
- **`POST-запросы`**: Отправка данных на сервер.
- **`PUT-запросы`**: Обновление существующих данных на сервере.
- **`DELETE-запросы`**: Удаление данных с сервера.

### Использование XMLHttpRequest

**XMLHttpRequest** — это старый API для выполнения асинхронных HTTP-запросов.

Несмотря на то что fetch является более современным и удобным вариантом, XMLHttpRequest все еще поддерживается.

#### 1. Создание запроса

```javascript
const xhr = new XMLHttpRequest();
xhr.open('GET', 'https://api.example.com/data', true);

xhr.onload = function() {
  if (xhr.status >= 200 && xhr.status < 300) {
    console.log(xhr.responseText);
  } else {
    console.error('Request failed');
  }
};

xhr.onerror = function() {
  console.error('Request error');
};

xhr.send();
```

#### 2. Отправка данных через POST-запрос

```javascript
const xhr = new XMLHttpRequest();
xhr.open('POST', 'https://api.example.com/submit', true);
xhr.setRequestHeader('Content-Type', 'application/json');

xhr.onload = function() {
  if (xhr.status >= 200 && xhr.status < 300) {
    console.log(xhr.responseText);
  } else {
    console.error('Request failed');
  }
};

xhr.onerror = function() {
  console.error('Request error');
};

const data = JSON.stringify({ name: 'John', age: 30 });
xhr.send(data);
```

### Использование fetch

**fetch** — это более современный API, который упрощает работу с HTTP-запросами и возвращает промис, что упрощает обработку асинхронных операций.

#### 1. Выполнение GET-запроса

```javascript
fetch('https://api.example.com/data')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // или response.text() для текстового ответа
  })
  .then(data => console.log(data))
  .catch(error => console.error('Fetch error:', error));
```

#### 2. Отправка данных через POST-запрос

```javascript
fetch('https://api.example.com/submit', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ name: 'John', age: 30 })
})
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // или response.text() для текстового ответа
  })
  .then(data => console.log(data))
  .catch(error => console.error('Fetch error:', error));
```

### Дополнительные примеры

#### 1. Обработка ошибок с fetch

```javascript
fetch('https://api.example.com/data')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error('Fetch error:', error));
```

#### 2. Отправка данных с дополнительными параметрами

```javascript
fetch('https://api.example.com/submit', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your-token'
  },
  body: JSON.stringify({ name: 'John', age: 30 })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Fetch error:', error));
```

### Выводы

Работа с веб-API через `XMLHttpRequest` и `fetch` позволяет взаимодействовать с сервером и обмениваться данными.

`fetch` является современным и удобным методом для выполнения HTTP-запросов и работы с асинхронными операциями, тогда как `XMLHttpRequest` может быть полезен в старых проектах или для определенных случаев.

Оба подхода позволяют выполнять запросы, обрабатывать ответы и управлять ошибками, что делает их важными инструментами для веб-разработки.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
