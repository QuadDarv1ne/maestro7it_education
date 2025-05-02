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
