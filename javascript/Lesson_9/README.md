# DOM: Манипуляция элементами веб-страницы

Манипуляция элементами веб-страницы с помощью JavaScript часто выполняется через работу с Document Object Model (DOM).

**Вот основные методы и техники для работы с DOM:**

### Поиск элементов в `DOM`

#### 1. `document.getElementById`

Этот метод возвращает элемент с указанным `id`.

```javascript
const element = document.getElementById('myElement');
```

#### 2. `document.getElementsByClassName`

Этот метод возвращает коллекцию элементов с указанным классом.

```javascript
const elements = document.getElementsByClassName('myClass');
```

#### 3. `document.getElementsByTagName`

Этот метод возвращает коллекцию элементов с указанным тегом.

```javascript
const elements = document.getElementsByTagName('div');
```

#### 4. `document.querySelector`

Этот метод возвращает первый элемент, который соответствует CSS-селектору.

```javascript
const element = document.querySelector('.myClass'); // Для первого элемента с классом 'myClass'
const element = document.querySelector('#myElement'); // Для элемента с id 'myElement'
```

#### 5. `document.querySelectorAll`

Этот метод возвращает коллекцию всех элементов, которые соответствуют CSS-селектору.

```javascript
const elements = document.querySelectorAll('.myClass');
```

### Изменение Содержимого и Стилей Элементов

#### 1. Изменение текста и HTML-содержимого

- **textContent:** Устанавливает или возвращает текстовое содержимое элемента.

```javascript
const element = document.getElementById('myElement');
element.textContent = 'New text content';
```

- **innerHTML:** Устанавливает или возвращает HTML-содержимое элемента.

```javascript
const element = document.getElementById('myElement');
element.innerHTML = '<p>New HTML content</p>';
```

#### 2. Изменение стилей

#### Изменение стиля через `style`

```javascript
const element = document.getElementById('myElement');
element.style.color = 'blue';
element.style.backgroundColor = 'yellow';
```

#### Добавление и удаление классов

```javascript
const element = document.getElementById('myElement');
element.classList.add('newClass'); // Добавляет класс
element.classList.remove('oldClass'); // Удаляет класс
element.classList.toggle('active'); // Переключает класс
```

### Работа с Cобытиями и Слушателями Событий

#### 1. Добавление слушателей событий

Используйте метод `addEventListener` для добавления обработчиков событий.

```javascript
const button = document.getElementById('myButton');

button.addEventListener('click', () => {
  alert('Button clicked!');
});
```

#### 2. Удаление слушателей событий

Используйте метод `removeEventListener` для удаления обработчиков событий.

```javascript
const handleClick = () => {
  alert('Button clicked!');
};

button.addEventListener('click', handleClick);
button.removeEventListener('click', handleClick);
```

#### 3. Обработка событий

Объект события `event` содержит информацию о событии, которое произошло.

Вы можете использовать его для доступа к различным свойствам и методам.

```javascript
button.addEventListener('click', (event) => {
  console.log(event.target); // Элемент, на который было произведено нажатие
  console.log(event.type); // Тип события, в данном случае 'click'
});
```

#### 4. Делегирование событий

Иногда полезно добавить один обработчик события к родительскому элементу и использовать его для обработки событий на дочерних элементах.

Это называется делегированием событий.

```javascript
document.getElementById('parent').addEventListener('click', (event) => {
  if (event.target && event.target.matches('button.child')) {
    console.log('Child button clicked!');
  }
});
```

---

### Выводы

Манипуляция `DOM` в JavaScript позволяет динамически изменять содержимое и стили веб-страниц, а также обрабатывать события.

Знание методов поиска элементов, изменения их свойств и обработки событий позволяет создавать интерактивные и динамичные веб-приложения.

---

**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
