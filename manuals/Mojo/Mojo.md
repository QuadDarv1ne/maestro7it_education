<a id="top"></a>

# Руководство по установке, настройке и запуску программ на Mojo

![Mojo](https://github.com/QuadDarv1ne/maestro7it_education/blob/cb7668e3765afb585151dfe56b7f056acdce0046/manuals/Mojo/img/Mojo.png)

**Полное пошаговое руководство.** Рассчитано в первую очередь на **Windows** (через `WSL 2`), но также подходит для `Linux` и `macOS`

[Официальная ссылка на Mojo](https://mojolang.org/) · [Extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=modular-mojotools.vscode-mojo)

---

## Содержание

1. [Что такое Mojo](#1-что-такое-mojo)
2. [Системные требования](#2-системные-требования)
3. [Установка на Windows через WSL 2](#3-установка-на-windows-через-wsl-2)
4. [Установка на Linux](#4-установка-на-linux)
5. [Установка на macOS](#5-установка-на-macos)
6. [Установка Mojo через pixi](#6-установка-mojo-через-pixi)
7. [Установка Mojo через uv](#7-установка-mojo-через-uv)
8. [Настройка окружения](#8-настройка-окружения)
9. [Код программы sysinfo.mojo](#9-код-программы-sysinfomojoo)
10. [Запуск программы sysinfo](#10-запуск-программы-sysinfo)
11. [Ожидаемый результат](#11-ожидаемый-результат)
12. [Дополнительные программы](#12-дополнительные-программы)
13. [Устранение неполадок](#13-устранение-неполадок)
14. [Полезные ссылки](#14-полезные-ссылки)

---

## 1. Что такое Mojo

**Mojo** — компилируемый, статически типизированный язык программирования от компании **Modular Inc.**, созданный Крисом Латтнером (автором `LLVM`, `Clang` и `Swift`). Он сочетает простоту синтаксиса `Python` с производительностью `C++` и `Rust`, ориентирован на задачи `ИИ`, научных вычислений и работу с `GPU`

**Ключевые особенности:**

- Синтаксис, вдохновлённый `Python` (отступы, `def`, `if`, `for`).
- Статическая типизация и полный контроль над памятью.
- Компиляция в нативный код через `MLIR`
- Поддержка `CPU`, `GPU` (`NVIDIA`, `AMD`, `Apple Silicon`).
- Полностью открытый исходный код (Apache 2.0 с исключениями).

[⬆ К содержанию](#содержание)

---

## 2. Системные требования

| Компонент | Требование |
|---|---|
| **Linux** | glibc 2.34+ (Ubuntu 22.04 LTS или новее) |
| **macOS** | macOS Sequoia (15) или новее, Apple Silicon (M1–M5) |
| **Windows** | Только через **WSL 2** с Ubuntu 22.04+ |
| **CPU** | x86-64-v3 (Haswell, ~2013 г.+) или ARM64 Neoverse N1+ |
| **RAM** | Минимум 8 ГБ |
| **GPU** | Опционально: NVIDIA (драйвер 580+), AMD, Apple Silicon |
| **Дополнительно** | Компилятор C (`gcc`, `clang`) на Linux; Xcode CLI Tools 16+ на macOS |

> ⚠️ **Важно для Windows:** нативная поддержка Windows **отсутствует**. Официальный путь — WSL 2 с Ubuntu

[⬆ К содержанию](#содержание)

---

## 3. Установка на Windows через WSL 2

### 3.1. Что такое WSL 2

**WSL 2** (Windows Subsystem for Linux) — это полноценное Linux-ядро внутри Windows. Оно позволяет запускать Ubuntu и другие дистрибутивы Linux без виртуальной машины.

### 3.2. Установка WSL 2 и Ubuntu

1. Откройте **PowerShell от имени администратора** (правый клик по «Пуск» → «Терминал (Администратор)»).
2. Выполните:

   ```powershell
   wsl --install -d Ubuntu
   ```

3. Дождитесь завершения установки. Перезагрузите компьютер, если потребуется.
4. После перезагрузки Ubuntu запустится автоматически. Введите **имя пользователя** (латиницей, строчными) и **пароль** (пароль при вводе не отображается — это нормально).
5. Обновите пакеты внутри Ubuntu:

   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

6. Установите необходимые инструменты сборки:

   ```bash
   sudo apt install -y build-essential curl git
   ```

### 3.3. Как открыть Ubuntu в дальнейшем

- Из меню «Пуск» найдите **Ubuntu** и запустите.
- Или из PowerShell: `wsl -d Ubuntu`.
- Или из Windows Terminal: выберите вкладку Ubuntu.

> 💡 **Совет:** установите [Windows Terminal](https://aka.ms/terminal) из Microsoft Store — он удобнее стандартной консоли и поддерживает вкладки.

### 3.4. Доступ к файлам Windows из Ubuntu

Диски Windows доступны в Ubuntu по пути `/mnt/`:

```bash
cd /mnt/c/Users/ВашеИмя/
```

Но **лучше создавать проекты внутри домашней папки Ubuntu** (`~/`), а не на диске Windows — это значительно быстрее.

```bash
mkdir -p ~/projects
cd ~/projects
```

### 3.5. Как открыть папку Ubuntu в проводнике Windows

В терминале Ubuntu выполните:

```bash
explorer.exe .
```

Откроется проводник с текущей папкой.

[⬆ К содержанию](#содержание)

---

## 4. Установка на Linux

Если вы уже используете Linux, пропустите раздел 3.

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y build-essential curl git
```

### Fedora

```bash
sudo dnf install -y gcc gcc-c++ curl git
```

### Arch

```bash
sudo pacman -S base-devel curl git
```

[⬆ К содержанию](#содержание)

---

## 5. Установка на macOS

1. Установите **Xcode Command Line Tools**:

   ```bash
   xcode-select --install
   ```

2. Примите лицензию (если требуется):

   ```bash
   sudo xcodebuild -license accept
   ```

3. Убедитесь, что `clang` доступен:

   ```bash
   clang --version
   ```

[⬆ К содержанию](#содержание)

---

## 6. Установка Mojo через pixi

**pixi** — рекомендуемый менеджер пакетов от разработчиков Mojo.

### 6.1. Установка pixi

В терминале Linux (Ubuntu в WSL, либо нативно на Linux/macOS):

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

После установки перезапустите оболочку:

```bash
source ~/.bashrc
```

> Для zsh используйте `source ~/.zshrc`.

Проверьте установку:

```bash
pixi --version
```

Должна отобразиться версия, например `pixi 0.40.0`

### 6.2. Настройка автодополнения (опционально)

Для **bash**:

```bash
eval "$(pixi completion --shell bash)"
```

Для **zsh**:

```bash
autoload -Uz compinit && compinit
eval "$(pixi completion --shell zsh)"
```

Чтобы сохранить автодополнение навсегда, добавьте соответствующую строку в конец `~/.bashrc` или `~/.zshrc`.

### 6.3. Создание проекта

```bash
pixi init sysinfo \
  -c https://conda.modular.com/max/ \
  -c conda-forge
cd sysinfo
```

### 6.4. Добавление Mojo

```bash
pixi add mojo
```

### 6.5. Активация окружения

```bash
pixi shell
```

Теперь в этом терминале доступна команда `mojo` — проверьте:

```bash
mojo --version
```

### 6.6. Выход из окружения

```bash
exit
```

[⬆ К содержанию](#содержание)

---

## 7. Установка Mojo через uv

Альтернативный способ — через менеджер пакетов **uv**.

### 7.1. Установка uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Перезапустите оболочку:

```bash
source ~/.bashrc
```

### 7.2. Создание проекта

```bash
uv init sysinfo
cd sysinfo
```

### 7.3. Добавление Mojo

```bash
uv add mojo
```

### 7.4. Активация окружения

```bash
source .venv/bin/activate
```

Проверьте:

```bash
mojo --version
```

[⬆ К содержанию](#содержание)

---

## 8. Настройка окружения

### 8.1. Расширение для VS Code

Для подсветки синтаксиса, автодополнения и отладки установите официальное расширение **Mojo** из:

- [Visual Studio Code Marketplace](https://marketplace.visualstudio.com/items?itemName=modular-mojotools.vscode-mojo)
- Open VSX Registry

После установки откройте любой `.mojo` файл — расширение автоматически найдёт SDK в активированном окружении.

### 8.2. Настройка GPU (опционально)

**NVIDIA с драйвером 580+**, **AMD** или **Apple Silicon** — дополнительная настройка не требуется.

**NVIDIA с драйвером старше 580** — укажите путь к компилятору `ptxas`:

```bash
export MODULAR_NVPTX_COMPILER_PATH=/usr/local/cuda/bin/ptxas
```

Добавьте строку в `~/.bashrc`, чтобы настройка сохранялась:

```bash
echo 'export MODULAR_NVPTX_COMPILER_PATH=/usr/local/cuda/bin/ptxas' >> ~/.bashrc
source ~/.bashrc
```

[⬆ К содержанию](#содержание)

---

## 9. Код программы `sysinfo.mojo`

Создайте файл в директории проекта:

```bash
nano sysinfo.mojo
```

Вставьте следующий код, сохраните (`Ctrl+O`, `Enter`) и выйдите (`Ctrl+X`):

```mojo
# sysinfo.mojo — Сбор информации о системе на Mojo
# Демонстрирует: sys.info, gpu.host, C FFI (external_call)

from std.sys.info import (
    os_is_linux, os_is_macos, os_is_windows,
    _current_cpu, _triple_attr,
    has_sse4, has_avx, has_avx2, has_avx512f,
    is_64bit
)
from std.sys import num_physical_cores, num_logical_cores
from std.ffi import external_call, c_long


# ── Вспомогательная функция: объём памяти в человекочитаемом виде ──
def format_bytes(bytes: Int) -> String:
    """Преобразует байты в строку вида '16.0 GB'."""
    var value = Float64(bytes)
    if value >= 1024.0 ** 3:
        return t"{round(value / (1024.0 ** 3), 2)} GB"
    elif value >= 1024.0 ** 2:
        return t"{round(value / (1024.0 ** 2), 2)} MB"
    else:
        return t"{round(value / 1024.0, 2)} KB"


# ── Секция 1: Операционная система и архитектура ──
def print_os_info():
    print("=" * 50)
    print("  ОПЕРАЦИОННАЯ СИСТЕМА И АРХИТЕКТУРА")
    print("=" * 50)

    var os_name = "Unknown"
    if os_is_linux():
        os_name = "Linux"
    elif os_is_macos():
        os_name = "macOS"
    elif os_is_windows():
        os_name = "Windows"

    var arch = String(_triple_attr())

    print(t"  ОС          : {os_name}")
    print(t"  Архитектура : {arch}")
    print(t"  64-битная   : {is_64bit()}")
    print()


# ── Секция 2: Информация о процессоре ──
def print_cpu_info():
    print("=" * 50)
    print("  ПРОЦЕССОР (CPU)")
    print("=" * 50)

    let cpu_model = String(_current_cpu())
    let phys_cores = num_physical_cores()
    let logic_cores = num_logical_cores()

    print(t"  Модель              : {cpu_model}")
    print(t"  Физических ядер     : {phys_cores}")
    print(t"  Логических потоков  : {logic_cores}")

    var features = String("")
    if has_sse4():
        features += " SSE4"
    if has_avx():
        features += " AVX"
    if has_avx2():
        features += " AVX2"
    if has_avx512f():
        features += " AVX-512"

    if len(features) > 0:
        print(t"  Наборы инструкций   :{features}")
    else:
        print("  Наборы инструкций   : не определены")
    print()


# ── Секция 3: Информация о видеокарте (GPU) ──
def print_gpu_info():
    print("=" * 50)
    print("  ВИДЕОКАРТА (GPU)")
    print("=" * 50)

    try:
        from gpu.host import DeviceContext, DeviceAttribute
        var ctx = DeviceContext()

        print(t"  Устройство          : {ctx.name()}")
        print(t"  API                 : {ctx.api()}")

        let (free_mem, total_mem) = ctx.get_memory_info()
        print(t"  Видеопамять (свободно): {format_bytes(Int(free_mem))}")
        print(t"  Видеопамять (всего)   : {format_bytes(Int(total_mem))}")

        let clock = ctx.get_attribute(DeviceAttribute.CLOCK_RATE)
        print(t"  Тактовая частота      : {clock} MHz")

        let max_blocks = ctx.get_attribute(DeviceAttribute.MAX_BLOCKS_PER_MULTIPROCESSOR)
        print(t"  Макс. блоков/SM      : {max_blocks}")

    except:
        print("  GPU не обнаружен или драйверы не поддерживаются.")
        print("  Mojo поддерживает NVIDIA, AMD и Apple Silicon GPU.")
    print()


# ── Секция 4: Оперативная память через C FFI ──
def print_ram_info():
    print("=" * 50)
    print("  ОПЕРАТИВНАЯ ПАМЯТЬ (RAM)")
    print("=" * 50)

    var phys_pages: c_long = 0
    var page_size: c_long = 0

    try:
        if os_is_linux():
            phys_pages = external_call["sysconf", c_long](c_long(85))
            page_size  = external_call["sysconf", c_long](c_long(30))
        elif os_is_macos():
            phys_pages = external_call["sysconf", c_long](c_long(200))
            page_size  = external_call["sysconf", c_long](c_long(29))

        if phys_pages > 0 and page_size > 0:
            let total_ram = Int(phys_pages) * Int(page_size)
            print(t"  Всего RAM   : {format_bytes(total_ram)}")

            if os_is_linux():
                try:
                    with open("/proc/meminfo", "r") as f:
                        for line in f:
                            if line.startswith("MemAvailable:"):
                                var parts = line.split()
                                if len(parts) >= 2:
                                    let free_kb = Int(parts[1])
                                    print(t"  Свободно    : {format_bytes(free_kb * 1024)}")
                                break
                except:
                    print("  Свободно    : (не удалось прочитать /proc/meminfo)")
        else:
            print("  Не удалось определить объём RAM через sysconf.")
    except:
        print("  Ошибка при запросе информации о RAM.")
    print()


# ── Точка входа ──
def main():
    print()
    print("╔" + "═" * 48 + "╗")
    print("║       СИСТЕМНАЯ ИНФОРМАЦИЯ (Mojo)             ║")
    print("╚" + "═" * 48 + "╝")
    print()

    print_os_info()
    print_cpu_info()
    print_gpu_info()
    print_ram_info()

    print("=" * 50)
    print("  Готово.")
    print("=" * 50)


if __name__ == "__main__":
    main()
```

[⬆ К содержанию](#содержание)

---

## 10. Запуск программы `sysinfo`

Из директории проекта (где лежит `sysinfo.mojo`):

### Способ 1: прямой запуск

```bash
mojo run sysinfo.mojo
```

Или короче:

```bash
mojo sysinfo.mojo
```

### Способ 2: через pixi (если окружение не активировано)

```bash
pixi run mojo sysinfo.mojo
```

### Способ 3: сборка в исполняемый файл

```bash
mojo build sysinfo.mojo -o sysinfo
./sysinfo
```

Готовый бинарник `sysinfo` появится в той же папке, где лежит `sysinfo.mojo`

[⬆ К содержанию](#содержание)

---

## 11. Ожидаемый результат

```
╔════════════════════════════════════════════════╗
║       СИСТЕМНАЯ ИНФОРМАЦИЯ (Mojo)             ║
╚════════════════════════════════════════════════╝

==================================================
  ОПЕРАЦИОННАЯ СИСТЕМА И АРХИТЕКТУРА
==================================================
  ОС          : Linux
  Архитектура : x86_64
  64-битная   : True

==================================================
  ПРОЦЕССОР (CPU)
==================================================
  Модель              : Intel(R) Core(TM) i7-12700K
  Физических ядер     : 12
  Логических потоков  : 20
  Наборы инструкций   : SSE4 AVX AVX2 AVX-512

==================================================
  ВИДЕОКАРТА (GPU)
==================================================
  Устройство          : NVIDIA GeForce RTX 4070
  API                 : CUDA
  Видеопамять (свободно): 8.45 GB
  Видеопамять (всего)   : 12.0 GB
  Тактовая частота      : 2475 MHz
  Макс. блоков/SM      : 24

==================================================
  ОПЕРАТИВНАЯ ПАМЯТЬ (RAM)
==================================================
  Всего RAM   : 32.0 GB
  Свободно    : 18.75 GB

==================================================
  Готово.
==================================================
```

> ℹ️ В `WSL 2` информация о `GPU` может отображаться иначе, чем в нативном Linux — это связано с пробросом устройств из Windows. Секция RAM будет работать корректно.

[⬆ К содержанию](#содержание)

---

## 12. Дополнительные программы

Помимо `sysinfo.mojo`, в проекте могут лежать ещё четыре программы. Каждая — отдельный файл, запускается независимо.

| Файл | Что делает |
|---|---|
| `mandelbrot.mojo` | Визуализация множества Мандельброта в ASCII |
| `benchmark.mojo` | Бенчмарк вычислительной производительности |
| `game_of_life.mojo` | Игра «Жизнь» Конвея с анимацией |
| `tictactoe.mojo` | Крестики-нолики с непобедимым ИИ (минимакс) |

### Запуск

**Убедитесь, что окружение активировано:**

```bash
pixi shell
```

Затем запускайте нужную программу:

```bash
# Визуализация фрактала Мандельброта
mojo mandelbrot.mojo

# Бенчмарк производительности
mojo benchmark.mojo

# Игра «Жизнь» Конвея
mojo game_of_life.mojo

# Крестики-нолики против ИИ
mojo tictactoe.mojo
```

[⬆ К содержанию](#содержание)

---

## 13. Устранение неполадок

| Проблема | Причина | Решение |
|---|---|---|
| `mojo: command not found` | Окружение не активировано | `pixi shell` или `source .venv/bin/activate` |
| `pixi: команда не найдена` в PowerShell | Попытка запустить Linux-команды в Windows | Откройте **Ubuntu** (WSL), а не PowerShell |
| `eval: команда не найдена` | Команда bash в PowerShell | Используйте bash/zsh, а не PowerShell |
| GPU-секция выдаёт ошибку | Нет дискретной GPU или драйверы старые | Проверьте драйверы; для NVIDIA < 580 задайте `MODULAR_NVPTX_COMPILER_PATH` |
| Ошибка импорта `gpu.host` | Устаревшая версия Mojo | `pixi update mojo` |
| Ошибка компиляции на старом CPU | Нет AVX2 | Проверьте: `grep -o avx2 /proc/cpuinfo \| head -1` |
| Медленная работа в WSL | Проект на диске Windows | Перенесите проект в `~/projects/` |
| Не отображается RAM | `sysconf` недоступен | На macOS/Linux — работает; на Windows — только через WSL |

### Диагностика окружения

**Проверьте ключевые компоненты:**

```bash
# Версия WSL (в PowerShell)
wsl --version

# Версия Ubuntu (в Ubuntu)
lsb_release -a

# Версия pixi
pixi --version

# Версия Mojo
mojo --version

# Поддержка AVX2
grep -o avx2 /proc/cpuinfo | head -1
```

[⬆ К содержанию](#содержание)

---

## 14. Полезные ссылки

- 🌐 Официальный сайт: [https://mojolang.org/](https://mojolang.org/)
- 📥 Установка: [https://mojolang.org/install/](https://mojolang.org/install/)
- 📚 Документация: [https://mojolang.org/docs/](https://mojolang.org/docs/)
- 💻 GitHub: [https://github.com/modular/mojo](https://github.com/modular/mojo)
- 🧩 VS Code Extension: [modular-mojotools.vscode-mojo](https://marketplace.visualstudio.com/items?itemName=modular-mojotools.vscode-mojo)
- 🐍 pixi: [https://pixi.sh/](https://pixi.sh/)
- ⚡ uv: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- 🐧 WSL 2: [https://learn.microsoft.com/windows/wsl/](https://learn.microsoft.com/windows/wsl/)

[⬆ К содержанию](#содержание)
