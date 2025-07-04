# Реализация алгоритма Евклида для вычисления НОД

## Описание проекта

**Этот проект содержит реализации алгоритма Евклида для вычисления наибольшего общего делителя (НОД) на трех языках программирования:** `C++`, `Go` и `Python`

## Требования
- **Для C++:** компилятор с поддержкой `C++17` (`g++ 7+` или `clang 5+`)
- **Для Go:** версия `Go 1.16+`
- **Для Python:** интерпретатор `Python 3.7+`

## Файлы проекта
1. `euclid_gcd.cpp` - реализация на `C++`
2. `euclid_gcd.go` - реализация на `Go`
3. `euclid_gcd.py` - реализация на `Python`

## Компиляция и запуск

### C++
```bash
g++ -std=c++17 euclid_gcd.cpp -o euclid_gcd
./euclid_gcd
```

### Go
```bash
go run euclid_gcd.go
```

### Python
```bash
python3 euclid_gcd.py
```

## Особенности реализации
- Запрос двух положительных целых чисел у пользователя
- Обработка некорректного ввода:
  * Отрицательные числа
  * Нечисловые значения
  * Неверное количество аргументов
- Корректная обработка случая (0, 0)
- Детализированные Docstrings для всех функций

## Примеры работы

### Корректный ввод
```
Введите два положительных целых числа: 48 18
НОД(48, 18) = 6
```

### Нулевые значения
```
Введите два положительных целых числа: 0 0
НОД(0, 0) не определён
```

### Обработка ошибок
```
Введите два положительных целых числа: -5 10
Ошибка! Введите положительные целые числа: abc 20
Ошибка! Введите положительные целые числа: 42
Ошибка! Введите положительные целые числа: 56 98
НОД(56, 98) = 14
```

## Автор
~ Реализация подготовлена в рамках учебного задания.

**Преподаватель:** Дуплей Максим Игоревич

**Дата:** 04.06.2025
