# Написание программы для получения данных о погоде

## Клиент для погодного API

- **Задача:** Напишите консольную утилиту, которая получает данные о погоде через `OpenWeatherMap API`

### Требования

- Принимать название города через аргументы.

- Выводить температуру, влажность и описание погоды.

- Кэшировать результаты на 10 минут (например, в файл `.weather_cache.json`).

#### Пример использования

```bash
$ go run weather.go -city=London
```

```textline
Температура: 15°C, Влажность: 72%, Описание: облачно
```

### Подсказки

- Используйте пакеты `net/http`, `encoding/json`, `os`

- Зарегистрируйтесь на `OpenWeatherMap` для получения API-ключа.

---

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram:** @quadd4rv1n7

📅 **Дата:** 02.05.2025

▶️ **Версия 1.0**

```textline
※ Предложения по сотрудничеству можете присылать на почту ※
📧 maksimqwe42@mail.ru
```
