**Для программы на ассемблере, особенно под `DOS`, принято использовать следующие соглашения:**

### 1. **Исходный файл:**

- **Назовите файл с расширением `.asm`, например:** `roman_calc.asm`

    (это стандартное расширение для исходников на ассемблере).

### 2. **Скомпилированный файл:**

- После компиляции через `NASM` вы получите `COM-файл` (из-за org `0x100`).

    **Назовите его так:** `roman_calc.com`

    (`COM-файлы` — это простые исполняемые файлы для `DOS`).

### Как скомпилировать

1. Установите `NASM` и `DOSBox`

2. В командной строке выполните:

    ```bash
    nasm roman_calc.asm -f bin -o roman_calc.com
    ```

3. Запустите в `DOSBox`:

    ```bash
    mount c: /ваш/путь/к/файлу
    c:
    roman_calc.com
    ```

### Почему именно так?

- `.asm` — стандартное расширение для исходников на ассемблере.

- `.com` — формат простых DOS-программ без заголовков (подходит для `org 0x100`).

- Имя `roman_calc` отражает суть программы («калькулятор римских чисел»).

---

**Преподаватель:** Дуплей Максим Игоревич

**Дата:** 14.04.2025
