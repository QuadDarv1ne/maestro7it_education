/**
 * Автор: Дуплей Максим Игоревич - AGLA
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
 * Проверяет, является ли число "некрасивым" (ugly number).
 * 
 * Некрасивое число - это положительное целое число, простые множители которого 
 * ограничены числами 2, 3 и 5.
 * 
 * @param {number} n - Число для проверки
 * @return {boolean} true, если число является некрасивым, иначе false
 * 
 * Алгоритм:
 * 1. Числа ≤ 0 не являются некрасивыми
 * 2. 1 считается некрасивым числом
 * 3. Последовательно делим число на 2, 3 и 5, пока это возможно
 * 4. Если после всех делений остаётся 1, число некрасивое
 * 
 * Примеры:
 *   isUgly(6)    // 6 = 2 × 3 → true
 *   isUgly(14)   // 14 = 2 × 7 → false
 * 
 * Сложность:
 *   Время: O(log n)
 *   Память: O(1)
 */
var isUgly = function(n) {
    if (n <= 0) {
        return false;
    }
    
    // Последовательно делим на разрешённые множители
    while (n % 2 === 0) {
        n /= 2;
    }
    while (n % 3 === 0) {
        n /= 3;
    }
    while (n % 5 === 0) {
        n /= 5;
    }
    
    // Если остался 1, значит других множителей нет
    return n === 1;
};