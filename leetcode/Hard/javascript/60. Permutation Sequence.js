/**
 * https://leetcode.com/problems/permutation-sequence/description/
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Permutation Sequence" на JavaScript
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

var getPermutation = function(n, k) {
    // Вычисляем факториалы
    const factorials = new Array(n).fill(1);
    for (let i = 1; i < n; i++) {
        factorials[i] = factorials[i-1] * i;
    }
    
    // Создаем список доступных чисел
    const numbers = [];
    for (let i = 1; i <= n; i++) {
        numbers.push(i);
    }
    
    let result = '';
    k--;  // Переход к 0-индексации
    
    for (let i = n - 1; i >= 0; i--) {
        const index = Math.floor(k / factorials[i]);
        k %= factorials[i];
        
        result += numbers[index].toString();
        numbers.splice(index, 1);
    }
    
    return result;
};