/*
LeetCode 3577: Count the Number of Computer Unlocking Permutations
https://leetcode.com/problems/count-the-number-of-computer-unlocking-permutations/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. YouTube канал: https://www.youtube.com/@it-coders
6. ВК группа: https://vk.com/science_geeks
*/

// ========================== C++ ==========================
class Solution {
public:
    /**
     * Подсчитывает количество валидных перестановок для разблокировки компьютеров.
     * 
     * Time Complexity: O(n)
     * Space Complexity: O(1)
     * 
     * @param complexity вектор сложностей паролей компьютеров
     * @return количество валидных перестановок по модулю 10^9 + 7
     */
    int countPermutations(vector<int>& complexity) {
        const int MOD = 1e9 + 7;
        int n = complexity.size();
        
        // Проверяем, можно ли разблокировать все компьютеры
        for (int i = 1; i < n; i++) {
            if (complexity[i] <= complexity[0]) {
                return 0;
            }
        }
        
        // Вычисляем (n-1)! mod MOD
        long long result = 1;
        for (int i = 1; i < n; i++) {
            result = (result * i) % MOD;
        }
        
        return static_cast<int>(result);
    }
};

/*
========================== ОБЪЯСНЕНИЕ АЛГОРИТМА ==========================

Задача:
- n компьютеров с метками 0..n-1, каждый с паролем сложности complexity[i]
- Компьютер 0 уже разблокирован
- Чтобы разблокировать компьютер i, нужен разблокированный компьютер j,
  где j < i и complexity[j] < complexity[i]

Решение:
1. Если любой компьютер i (i > 0) имеет complexity[i] <= complexity[0]:
   → Невозможно разблокировать (возвращаем 0)
   
2. Иначе все компьютеры имеют сложность > complexity[0]:
   → Любая перестановка работает
   → Ответ = (n-1)! mod 10^9+7

Почему это работает?
- Компьютер 0 может разблокировать ЛЮБОЙ компьютер с большей сложностью
- После разблокировки компьютера, он тоже может разблокировать другие
- Поэтому ЛЮБОЙ порядок разблокировки валиден

Примеры:
1. [1, 2, 3] → 2! = 2 (перестановки: [0,1,2], [0,2,1])
2. [2, 1, 3] → 0 (компьютер 1 не может быть разблокирован)
3. [1, 2, 3, 4, 5] → 4! = 24

Сложность:
- Время: O(n) - проход по массиву + вычисление факториала
- Память: O(1) - константная память

Ключевые моменты реализации:
- Java/C#: long для промежуточных вычислений, приведение к int в конце
- C++: long long для вычислений, static_cast<int> в конце
- JavaScript: автоматическое управление типами, но будьте осторожны с большими числами
- Все языки: используем модуль 10^9+7 на каждой итерации для предотвращения переполнения
*/