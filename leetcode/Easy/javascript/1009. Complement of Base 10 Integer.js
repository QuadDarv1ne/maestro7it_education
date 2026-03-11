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
 * Находит дополнение целого числа (инверсия всех битов).
 * 
 * @param {number} n - Входное неотрицательное целое число (0 <= n < 10^9)
 * @return {number} Дополнение числа n
 * 
 * @description
 * Алгоритм: Битовая инверсия с использованием маски.
 * 
 * Шаги:
 * 1. Обработать крайний случай: n === 0 → вернуть 1
 * 2. Найти количество значимых бит: bit_length
 * 3. Создать маску: mask = (1 << bit_length) - 1
 * 4. Инвертировать: result = n ^ mask
 * 
 * Пример:
 *   n = 5 (бинарно: 101)
 *   bit_length = 3
 *   mask = (1 << 3) - 1 = 7 (бинарно: 111)
 *   result = 5 ^ 7 = 2 (бинарно: 010) ✓
 * 
 * Сложность:
 *   Время: O(1) — максимум 30 бит для n < 10^9
 *   Память: O(1)
 * 
 * @example
 * // Вход: n = 5
 * // Выход: 2
 * // Объяснение: 5 → "101" → инверсия "010" → 2
 */
var bitwiseComplement = function(n) {
    // Крайний случай: дополнение 0 равно 1
    if (n === 0) return 1;
    
    // Находим количество значимых бит
    // toString(2) конвертирует число в двоичную строку
    const bit_length = n.toString(2).length;
    
    // Создаём маску из единиц нужной длины
    // (1 << bit_length) даёт 1000...0, вычитаем 1 → 0111...1
    const mask = (1 << bit_length) - 1;
    
    // XOR инвертирует все биты в пределах маски
    return n ^ mask;
};