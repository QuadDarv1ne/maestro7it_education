# Написание программы для шифрования файлов через AES

## Шифрование файлов с использованием AES

- **Задача:** Реализуйте утилиту для шифрования и дешифрования файлов с алгоритмом `AES-256`

### Требования

- Принимать путь к файлу, пароль и режим (`encrypt`/`decrypt`) через аргументы.

- Генерировать ключ из пароля с использованием `PBKDF2`

- Сохранять зашифрованные данные в новый файл (например, `file.txt.enc`).

### Пример использования

```bash
go mod init github.com/quadd4rv1n7/crypto_algorithm
go mod tidy
```

```bash
# Шифрование
go run crypto_algorithm.go -file secret.txt -password "12345" -mode encrypt

# Дешифрование
go run crypto_algorithm.go -file secret.txt.enc -password "12345" -mode decrypt
```

```bash
# Убедитесь, что файл .enc не был изменен или поврежден.
# Размер файла должен быть больше 8 байт.
Get-Item secret.txt.enc | Select-Object Length
```

```bash
# При дешифровании первые 8 байт файла — это соль.
// В разделе дешифрования добавьте:
fmt.Printf("Salt (hex): %x\n", salt)

// В разделе шифрования после генерации соли:
fmt.Printf("[ENCRYPT] Salt (hex): %x\n", salt)

// В разделе дешифрования после извлечения соли:
fmt.Printf("[DECRYPT] Salt (hex): %x\n", salt)
fmt.Printf("[DECRYPT] Data length: %d bytes\n", len(data[8:]))
```

#### Тестовый сценарий

```bash
# Добавьте путь в PATH через PowerShell (временно)
$env:Path += ";C:\Program Files\Go\bin"
```

```bash
# 1. Создайте тестовый файл
echo "Hello, World!" > test.txt

# 2. Зашифруйте
go run crypto_algorithm.go -file test.txt -password "12345" -mode encrypt

# 3. Дешифруйте
go run crypto_algorithm.go -file test.txt.enc -password "12345" -mode decrypt

# 4. Проверьте результат
Get-Content test.txt.dec
```

### Подсказки

- Используйте пакеты `crypto/aes`, `crypto/cipher`, `crypto/rand`

- Добавьте соль (`salt`) для усиления безопасности.

---

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram:** @quadd4rv1n7

📅 **Дата:** 02.05.2025

▶️ **Версия 1.0**

```textline
※ Предложения по сотрудничеству можете присылать на почту ※
📧 maksimqwe42@mail.ru
```
