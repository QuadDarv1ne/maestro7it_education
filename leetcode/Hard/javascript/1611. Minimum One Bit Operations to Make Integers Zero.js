/*
https://leetcode.com/problems/minimum-one-bit-operations-to-make-integers-zero/description/?envType=daily-question&envId=2025-11-08
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
*/

/**
 * @param {number} n
 * @return {number}
 */
var minimumOneBitOperations = function(n) {
    // Преобразование в код Грея (Gray code)
    // Количество операций = n XOR (n >> 1) XOR (n >> 2) XOR ...
    let result = 0;
    while (n !== 0) {
        result ^= n;
        n >>= 1;
    }
    return result;
};

/* 
Альтернативное решение через рекурсию с мемоизацией:

var minimumOneBitOperations = function(n) {
    const memo = new Map();
    
    function solve(num) {
        if (num === 0) return 0;
        if (memo.has(num)) return memo.get(num);
        
        // Находим позицию старшего бита
        let msb = 0;
        let temp = num;
        while (temp !== 0) {
            temp >>= 1;
            msb++;
        }
        msb--;
        
        // Формула: f(n) = 2^(msb+1) - 1 - f(n XOR 2^msb)
        const result = (1 << (msb + 1)) - 1 - solve(num ^ (1 << msb));
        memo.set(num, result);
        return result;
    }
    
    return solve(n);
};

Пошаговый пример для n = 6 (двоичное: 110):
1. result = 0, n = 6 (110)
2. result = 0 XOR 6 = 6, n = 3 (11)
3. result = 6 XOR 3 = 5, n = 1 (1)
4. result = 5 XOR 1 = 4, n = 0
5. Ответ: 4

Ключевые моменты:
- Используем побитовый XOR (^) и сдвиг вправо (>>)
- Алгоритм основан на свойствах кода Грея
- Очень эффективное решение: O(log n) время, O(1) память
*/

/* Полезные ссылки: */
// 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
// 2. Telegram №1 @quadd4rv1n7
// 3. Telegram №2 @dupley_maxim_1999
// 4. Rutube канал: https://rutube.ru/channel/4218729/
// 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
// 6. YouTube канал: https://www.youtube.com/@it-coders
// 7. ВК группа: https://vk.com/science_geeks