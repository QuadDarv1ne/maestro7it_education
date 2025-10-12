# Создание инженерного калькулятора

### 🛠 Как собрать проект с помощью CMake

**Откройте терминал в корне проекта (где лежит `CMakeLists.txt`) и выполните:**

```bash
mkdir build
cd build
cmake ..
cmake --build .
```

**После этого в папке `build/` появится исполняемый файл:**

- Linux/macOS: `engineering-calculator`

- Windows (с `MSVC` или `MinGW`): `engineering-calculator.exe`

**Запустите его:**

```bash
./engineering-calculator
```

### 🛠 Вариант 2: Соберите без CMake (вручную)

Если не хотите ставить `CMake`, можно скомпилировать напрямую через `g++` или `cl.exe`

**Если у вас установлен MinGW-w64 (например, через MSYS2 или standalone):**

```powershell
g++ -std=c++17 -O2 -Wall -o engineering-calculator.exe main.cpp Calculator.cpp Tokenizer.cpp
.\engineering-calculator.exe
```

> Убедитесь, что g++ доступен: g++ --version

**Если у вас только `Visual Studio`, но нет `g++` используйте `cl.exe` в `Developer PowerShell`:**

```powershell
cl /EHsc /std:c++17 /O2 main.cpp Calculator.cpp Tokenizer.cpp
engineering-calculator.exe
```

---

## Контакты

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)

📧 **Email:** [maksimqwe42@mail.ru](mailto:maksimqwe42@mail.ru)

📅 **Дата:** 12.10.2025

▶️ **Версия:** 1.0

```printtext
※ Предложения по сотрудничеству можете присылать на почту ※
📧 maksimqwe42@mail.ru
```
