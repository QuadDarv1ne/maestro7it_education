# Temperature Converter 🌡️

CLI-утилита для конвертации температур между шкалами Цельсия, Фаренгейта и Кельвина.

## Использование

```bash
$ go run cmd/converter/main.go -from=C -to=F -value=25
```

```bash
77.00°F
```

### Флаги

- -from: Исходная шкала (C, F, K).

- -to: Целевая шкала (C, F, K).

- -value: Значение температуры.

### Особенности

- Валидация шкал и значений.

- Округление результата до 2 знаков.

- Защита от отрицательных значений Кельвина.

---

### **Как запустить**

1. Установите зависимости:
   ```bash
   go mod init github.com/your-username/temperature-converter
   go mod tidy
   ```

2. Соберите и запустите:
   ```bash
   go run cmd/converter/main.go -from=K -to=C -value=300
   ```

### Структура проекта

```textline
temperature-converter/  
├── cmd/  
│   └── converter/          # CLI-утилита  
│       └── main.go         # Точка входа  
├── internal/  
│   └── converter/          # Логика конвертации  
│       ├── temperature.go  # Типы и валидация  
│       └── convert.go      # Формулы и вычисления  
└── README.md               # Описание проекта 
```

---

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram:** @quadd4rv1n7

📅 **Дата:** 01.05.2025

▶️ **Версия 1.0**

```textline
※ Предложения по сотрудничеству можете присылать на почту ※
📧 maksimqwe42@mail.ru
```
