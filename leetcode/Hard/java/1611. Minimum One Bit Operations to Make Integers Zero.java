/*
https://leetcode.com/problems/minimum-one-bit-operations-to-make-integers-zero/description/?envType=daily-question&envId=2025-11-08
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
*/

class Solution {
    public int minimumOneBitOperations(int n) {
        // Преобразование в код Грея (Gray code)
        // Количество операций = n XOR (n >> 1) XOR (n >> 2) XOR ...
        int result = 0;
        while (n != 0) {
            result ^= n;
            n >>= 1;
        }
        return result;
    }
}

/* 
Альтернативное решение через рекурсию с мемоизацией:

class Solution {
    private Map<Integer, Integer> memo = new HashMap<>();
    
    public int minimumOneBitOperations(int n) {
        if (n == 0) return 0;
        if (memo.containsKey(n)) return memo.get(n);
        
        // Находим позицию старшего бита
        int msb = 0;
        int temp = n;
        while (temp != 0) {
            temp >>= 1;
            msb++;
        }
        msb--;
        
        // Формула: f(n) = 2^(msb+1) - 1 - f(n XOR 2^msb)
        int result = (1 << (msb + 1)) - 1 - minimumOneBitOperations(n ^ (1 << msb));
        memo.put(n, result);
        return result;
    }
}

Математическая основа:
Код Грея - это система двоичного кодирования, где два последовательных 
значения отличаются только в одном бите. Минимальное количество операций 
для преобразования числа n в 0 равно обратному преобразованию кода Грея.

Сложность:
- Время: O(log n) - проходим по всем битам числа
- Память: O(1) - используем только переменные
*/

/* Полезные ссылки: */
// 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
// 2. Telegram №1 @quadd4rv1n7
// 3. Telegram №2 @dupley_maxim_1999
// 4. Rutube канал: https://rutube.ru/channel/4218729/
// 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
// 6. YouTube канал: https://www.youtube.com/@it-coders
// 7. ВК группа: https://vk.com/science_geeks