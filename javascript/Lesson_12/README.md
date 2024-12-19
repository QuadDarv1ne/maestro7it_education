# Работа с LocalStorage и SessionStorage

`LocalStorage` и `SessionStorage` — это две встроенные технологии для хранения данных в браузере.

Они позволяют сохранять данные в веб-приложениях без необходимости обращения к серверу.

### Основы хранения данных в браузере:

- **LocalStorage:** Предназначен для долговременного хранения данных. Данные сохраняются в браузере даже после закрытия вкладки или браузера. Размер хранилища обычно ограничен (обычно 5-10 МБ в зависимости от браузера).

- **SessionStorage:** Предназначен для хранения данных, которые должны сохраняться только в рамках одной сессии. Данные исчезают, когда вкладка или окно браузера закрывается. Размер хранилища такой же, как у LocalStorage.

Обе технологии используют ключ-значение для хранения данных.

### Чтение и Запись данных в `LocalStorage`

#### 1. Запись данных

Для записи данных в `LocalStorage` используется метод `setItem`. Ключ и значение должны быть строками.

```javascript
// Запись данных в LocalStorage
localStorage.setItem('username', 'JohnDoe');
```

#### 2. Чтение данных

Для чтения данных используется метод `getItem`. Если ключ не существует, возвращается `null`.

```javascript
// Чтение данных из LocalStorage
const username = localStorage.getItem('username');
console.log(username); // JohnDoe
```

#### 3. Удаление данных

Для удаления данных используется метод `removeItem`. Это удаляет только значение по указанному ключу.

```javascript
// Удаление данных из LocalStorage
localStorage.removeItem('username');
```

#### 4. Очистка всех данных

Для очистки всех данных в `LocalStorage` используется метод `clear`.

```javascript
// Очистка всех данных из LocalStorage
localStorage.clear();
```

### Использование SessionStorage

#### 1. Запись данных

Запись данных в `SessionStorage` выполняется аналогично `LocalStorage`.

```javascript
// Запись данных в SessionStorage
sessionStorage.setItem('sessionID', 'abc123');
```

#### 2. Чтение данных

Чтение данных из `SessionStorage` аналогично чтению из `LocalStorage`.

```javascript
// Чтение данных из SessionStorage
const sessionID = sessionStorage.getItem('sessionID');
console.log(sessionID); // abc123
```

#### 3. Удаление данных

Удаление данных из `SessionStorage` выполняется также, как и для `LocalStorage`.

```javascript
// Удаление данных из SessionStorage
sessionStorage.removeItem('sessionID');
```

4. Очистка всех данных

Очистка всех данных из `SessionStorage` также осуществляется с помощью метода `clear`.

```javascript
// Очистка всех данных из SessionStorage
sessionStorage.clear();
```

### Примеры использования

#### 1. Сохранение пользовательских настроек

```javascript
// Сохранение настроек пользователя
function saveUserSettings(theme, fontSize) {
  localStorage.setItem('theme', theme);
  localStorage.setItem('fontSize', fontSize);
}

// Пример использования
saveUserSettings('dark', '16px');
```

#### 2. Восстановление настроек при загрузке страницы

```javascript
// Восстановление настроек пользователя
function loadUserSettings() {
  const theme = localStorage.getItem('theme');
  const fontSize = localStorage.getItem('fontSize');

  if (theme) {
    document.body.className = theme;
  }
  if (fontSize) {
    document.body.style.fontSize = fontSize;
  }
}

// Пример использования
window.onload = loadUserSettings;
```

#### 3. Отслеживание активности пользователя (сессия)

```javascript
// Установка таймера сессии
function startSessionTimer() {
  sessionStorage.setItem('sessionStart', new Date().toISOString());
}

// Проверка активности
function checkSessionActivity() {
  const sessionStart = sessionStorage.getItem('sessionStart');
  if (sessionStart) {
    const startTime = new Date(sessionStart);
    const currentTime = new Date();
    const elapsedTime = Math.floor((currentTime - startTime) / 1000); // в секундах

    console.log(`Session started ${elapsedTime} seconds ago`);
  }
}

// Пример использования
startSessionTimer();
setTimeout(checkSessionActivity, 5000); // Проверка через 5 секунд
```

---

### Выводы

`LocalStorage` и `SessionStorage` являются мощными инструментами для хранения данных в браузере.

LocalStorage подходит для хранения данных, которые должны быть доступны между сессиями, в то время как SessionStorage удобен для временных данных, которые должны исчезнуть при закрытии вкладки или окна браузера.

Эти технологии просты в использовании и позволяют улучшить взаимодействие пользователя с веб-приложением.

---

**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
