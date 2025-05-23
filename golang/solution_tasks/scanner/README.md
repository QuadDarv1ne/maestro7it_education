# Написание программы сканера портов

## Параллельный сканер портов

- Задача: Напишите программу, которая сканирует диапазон портов на указанном хосте, используя горутины и каналы для параллельной обработки.

### Требования

- Принимать адрес хоста и диапазон портов (например, 80-1000) через аргументы командной строки.

- Проверять доступность портов асинхронно (TCP/UDP).

- Выводить результат в формате: [OPEN] 127.0.0.1:8080.

### Пример использования

```bash
$ go run scanner.go 127.0.0.1 80-500
```

### Подсказки

- Используйте пакеты `net`, `sync`, `strings`

- Ограничьте количество одновременных горутин (например, 100).

---

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram:** @quadd4rv1n7

📅 **Дата:** 02.05.2025

▶️ **Версия 1.0**

```textline
※ Предложения по сотрудничеству можете присылать на почту ※
📧 maksimqwe42@mail.ru
```
