# Написание программы для генератора QR-кодов с настройкой цвета

## 🔐 Реализация генератора QR-кодов с настройкой цвета

### Файлы

- `qrgen.go` — основной код

### 🎯 Требования

1. Генерация `QR-кодов` из `текста/URL`

2. **Настройка цветов:**
    - Цвет QR-кода
    - Цвет фона

3. **Сохранение в форматах:** `PNG`, `JPEG`
4. Поддержка размеров (`200x200`, `500x500` и `т.д.`).

### 🚀 Запуск

```bash
# Добавьте путь в PATH через PowerShell (временно)
$env:Path += ";C:\Program Files\Go\bin"
```

```bash
go mod init github.com/quadd4rv1n7/qr-code-generator
go mod tidy
```

```bash
go get github.com/skip2/go-qrcode

# Красный QR-код + Зелёный фон
go run qr-code-gen.go -content "https://school-maestro7it.ru/" -output school-maestro7it.png -fg "#0000CD" -bg "#000000" -size 400 -radius 50

# Синий QR-код + Белый фон
go run qr-code-gen.go -content "https://school-maestro7it.ru/" -output school-maestro7it.png -fg "#0000CD" -bg "#FFFFFF" -size 400 -radius 50
```

### 🌟 Фичи

- **Поддержка HEX-цветов:**

```bash
-fg "#FF0000" # Красный QR-код
-bg "#00FF00" # Зелёный фон

-fg "#0000CD" # Синий QR-код
-bg "#000000" # Белый фон

```

- **Градации качества:**

- - `qrcode.Low` (15% избыточности)
- - `qrcode.Highest` (30% избыточности)

### 💡 Примеры использования

1. **Визитка:**

```bash
go run qrgen.go -content "BEGIN:VCARD...END:VCARD" -output contact.png
```

2. **Wi-Fi доступ:**

```bash
go run qrgen.go -content "WIFI:S:MyNetwork;T:WPA;P:Password;;" -fg "#0000FF"
```

### 🔧 Возможные улучшения

1. Добавьте логотип в центр `QR-кода`
2. Реализуйте `GUI-версию` с помощью `Fyne` или `Wails`
3. `Поддержка SVG-формата`

---

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram:** @quadd4rv1n7

📅 **Дата:** 02.05.2025

▶️ **Версия 1.0**

```textline
※ Предложения по сотрудничеству можете присылать на почту ※
📧 maksimqwe42@mail.ru
```
