# Средний элемент (Median Out Of Three)

## 1. Постановка задачи

**Платформа:** [CodeRun — Яндекс](https://coderun.yandex.ru/problem/median-out-of-three)  
**Сложность:** Лёгкая  
**Темы:** сортировка, условные операторы, базовая математика

**Дано:** три целых числа.  
**Найти:** медиану — число, которое окажется на втором месте после упорядочивания трёх чисел по неубыванию.

**Формат ввода:** одна строка, содержащая три целых числа, разделённых пробелами.  
**Формат вывода:** одно целое число — медиана.

**Примеры:**

| Ввод | Вывод |
|:----:|:-----:|
| `1 2 3` | `2` |
| `1000 -1000 0` | `0` |

---

## 2. Идея решения

Медиана трёх чисел — это всегда «среднее» по величине. Существует три классических подхода:

1. **Сортировка трёх элементов** — упорядочить и взять элемент с индексом 1. Самый лаконичный и читаемый.
2. **Формула через min/max** — медиана = сумма всех трёх − минимум − максимум.
3. **Перебор перестановок** — явно проверить все 6 возможных порядков и вернуть средний элемент.

Для задачи с фиксированным количеством элементов (ровно 3) все три подхода работают за константное время O(1). В решениях ниже используется наиболее идиоматичный для каждого языка способ.

---

## 3. Разбор кода

### Python

```python
"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

def median_of_three(a: int, b: int, c: int) -> int:
    """
    Возвращает медиану трёх целых чисел.

    Алгоритм: упорядочиваем три числа и берём средний элемент.
    Для фиксированного набора из 3 элементов сортировка работает за O(1).

    Args:
        a: Первое целое число.
        b: Второе целое число.
        c: Третье целое число.

    Returns:
        Медиана — среднее по величине число.

    Examples:
        >>> median_of_three(1, 2, 3)
        2
        >>> median_of_three(1000, -1000, 0)
        0
    """
    return sorted([a, b, c])[1]


def main() -> None:
    """
    Считывает три целых числа из стандартного ввода
    и выводит их медиану.
    """
    data = input().strip().split()
    a, b, c = map(int, data)
    print(median_of_three(a, b, c))


if __name__ == "__main__":
    main()
```

**Почему именно так:** `sorted([a, b, c])` создаёт список из трёх элементов, сортирует их (Timsort на 3 элементах — это просто несколько сравнений) и возвращает элемент с индексом `[1]`. Код максимально читаемый и «питоничный».

---

### C++

```cpp
/**
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

#include <bits/stdc++.h>
using namespace std;

/**
 * @brief Возвращает медиану трёх целых чисел.
 * 
 * Алгоритм: помещаем числа в массив из 3 элементов,
 * сортируем стандартной функцией sort (для 3 элементов — константное время)
 * и возвращаем средний элемент.
 * 
 * @param a Первое целое число.
 * @param b Второе целое число.
 * @param c Третье целое число.
 * @return int Медиана — среднее по величине число.
 * 
 * @example
 *   medianOfThree(1, 2, 3);   // возвращает 2
 *   medianOfThree(5, 1, 3);   // возвращает 3
 */
int medianOfThree(int a, int b, int c) {
    int arr[3] = {a, b, c};
    sort(arr, arr + 3);
    return arr[1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int a, b, c;
    if (cin >> a >> b >> c) {
        cout << medianOfThree(a, b, c) << '\n';
    }
    return 0;
}
```

**Почему именно так:** `std::sort` на фиксированном массиве из 3 элементов компилятор оптимизирует до нескольких сравнений и swap'ов. `ios::sync_with_stdio(false); cin.tie(nullptr);` — стандартное ускорение ввода-вывода для CodeRun.

---

### Java

```java
/**
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

import java.util.Scanner;
import java.util.Arrays;

/**
 * Класс для решения задачи "Средний элемент".
 * 
 * Медиана трёх чисел — это число, которое оказывается на втором месте
 * после сортировки трёх элементов по возрастанию.
 */
public class MedianOutOfThree {

    /**
     * Вычисляет медиану трёх целых чисел.
     * 
     * Алгоритм: упорядочиваем три числа в массиве и возвращаем средний элемент.
     * Для массива длиной 3 сортировка выполняется за константное время.
     * 
     * @param a Первое целое число.
     * @param b Второе целое число.
     * @param c Третье целое число.
     * @return Медиана — среднее по величине число.
     * 
     * Примеры:
     *   medianOfThree(1, 2, 3) возвращает 2
     *   medianOfThree(7, 3, 5) возвращает 5
     */
    public static int medianOfThree(int a, int b, int c) {
        int[] arr = {a, b, c};
        Arrays.sort(arr);
        return arr[1];
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int a = scanner.nextInt();
        int b = scanner.nextInt();
        int c = scanner.nextInt();

        System.out.println(medianOfThree(a, b, c));

        scanner.close();
    }
}
```

**Почему именно так:** `Arrays.sort(int[])` для 3 элементов использует быструю сортировку с оптимизациями, фактически сводясь к паре сравнений. Альтернатива — формула `a + b + c - Math.min(a, Math.min(b, c)) - Math.max(a, Math.max(b, c))`, но сортировка массива читается понятнее.

---

### C#

```csharp
/**
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

using System;
using System.Linq;

/**
 * Класс для решения задачи "Средний элемент" (Median Out Of Three).
 * 
 * Задача: найти медиану трёх целых чисел — число, которое окажется
 * на втором месте после упорядочивания по возрастанию.
 */
class Program
{
    /**
     * Вычисляет медиану трёх целых чисел.
     * 
     * Алгоритм: помещаем числа в массив, сортируем и берём элемент с индексом 1.
     * Для фиксированного размера 3 операция сортировки работает за O(1).
     * 
     * @param a Первое целое число.
     * @param b Второе целое число.
     * @param c Третье целое число.
     * @return Медиана — среднее по величине число.
     * 
     * Примеры:
     *   MedianOfThree(1, 2, 3) возвращает 2
     *   MedianOfThree(-5, 10, 0) возвращает 0
     */
    static int MedianOfThree(int a, int b, int c)
    {
        int[] arr = { a, b, c };
        Array.Sort(arr);
        return arr[1];
    }

    static void Main()
    {
        string[] tokens = Console.ReadLine().Split();
        int a = int.Parse(tokens[0]);
        int b = int.Parse(tokens[1]);
        int c = int.Parse(tokens[2]);

        Console.WriteLine(MedianOfThree(a, b, c));
    }
}
```

**Почему именно так:** `Array.Sort` в .NET для массива из 3 элементов использует оптимизированный алгоритм. LINQ-вариант (`new[]{a,b,c}.OrderBy(x=>x).ElementAt(1)`) выглядит изящно, но создаёт лишние allocations; ручная сортировка массива предпочтительнее в олимпиадном коде.

---

### JavaScript (Node.js)

```javascript
/**
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

/**
 * Возвращает медиану трёх целых чисел.
 * 
 * Алгоритм: упорядочиваем три числа в массиве и возвращаем средний элемент.
 * Для массива длиной 3 сортировка выполняется за константное время.
 * 
 * @param {number} a - Первое целое число.
 * @param {number} b - Второе целое число.
 * @param {number} c - Третье целое число.
 * @returns {number} Медиана — среднее по величине число.
 * 
 * @example
 * medianOfThree(1, 2, 3);   // 2
 * medianOfThree(5, 1, 3);   // 3
 */
function medianOfThree(a, b, c) {
    return [a, b, c].sort((x, y) => x - y)[1];
}

/**
 * Основная функция: считывает три числа из stdin и выводит медиану.
 */
function main() {
    const input = require('fs').readFileSync(0, 'utf-8').trim().split(/\s+/);
    const a = parseInt(input[0], 10);
    const b = parseInt(input[1], 10);
    const c = parseInt(input[2], 10);

    console.log(medianOfThree(a, b, c));
}

main();
```

**Почему именно так:** `[a, b, c].sort((x, y) => x - y)` создаёт массив из 3 элементов и сортирует его численно (важно передать компаратор, иначе сортировка лексикографическая). Чтение через `readFileSync(0)` — стандартный способ быстрого ввода в Node.js для CodeRun.

---

## 4. Пример работы

**Входные данные:**
```
5 1 3
```

**Пошаговая трассировка:**

| Шаг | Действие | Результат |
|:---:|:---------|:---------:|
| 1 | Создаём массив `[5, 1, 3]` | `[5, 1, 3]` |
| 2 | Сортируем | `[1, 3, 5]` |
| 3 | Берём элемент с индексом 1 | `3` |

**Выходные данные:**
```
3
```

---

## 5. Асимптотическая сложность

**Время:** O(1)  
Сортировка фиксированного массива из 3 элементов выполняется за константное количество сравнений (не более 3), независимо от величины чисел.

**Память:** O(1)  
Используется массив из 3 элементов и несколько переменных — фиксированный объём памяти.

---

## 6. Почему решение оптимально?

1. **Нижняя граница.** Для нахождения медианы трёх чисел необходимо установить порядок между ними, что требует минимум 2–3 сравнения. Любое корректное решение не может быть асимптотически быстрее O(1), и наше решение достигает этой границы.

2. **Читаемость.** Использование встроенной сортировки для 3 элементов делает код понятным с первого взгляда. Читатель сразу видит намерение: «взять средний из трёх».

3. **Универсальность.** Подход масштабируется: если бы задача требовала медианы 5 чисел, код изменился бы минимально (`sorted(arr)[2]`).

---

## 7. Возможные улучшения и замечания

- **Формула min/max.** Вместо сортировки можно использовать:
  ```python
  return a + b + c - min(a, b, c) - max(a, b, c)
  ```
  Это тоже O(1), но избегает создания массива. В Python разница несущественна, в C++ может дать небольшой выигрыш.

- **Ручное сравнение.** Для максимальной производительности на микроуровне можно написать:
  ```cpp
  int median(int a, int b, int c) {
      if (a > b) swap(a, b);
      if (b > c) swap(b, c);
      if (a > b) swap(a, b);
      return b;
  }
  ```
  Это гарантированно 3 сравнения и до 3 обменов, без накладных расходов вызова `sort`.

- **Обработка одинаковых чисел.** Все представленные решения корректно работают при равных числах (например, `5 5 5` → `5`, `2 2 3` → `2`), так как используют нестрогий порядок сортировки.

---

## 8. Об авторе

| Ресурс | Ссылка |
|:-------|:-------|
| ORCID | [0009-0007-7605-539X](https://orcid.org/0009-0007-7605-539X) |
| GitHub | [QuadDarv1ne](https://github.com/QuadDarv1ne/) |
| Telegram | [Хижина программиста Æ](https://t.me/hut_programmer_07) |
| Rutube | [Канал](https://rutube.ru/channel/4218729/) |
| Plvideo | [Канал](https://plvideo.ru/channel/AUPv_p1r5AQJ) |
| YouTube | [@it-coders](https://www.youtube.com/@it-coders) |
| ВК | [science_geeks](https://vk.com/science_geeks) |

> **Дуплей Максим Игоревич — AGLA**
