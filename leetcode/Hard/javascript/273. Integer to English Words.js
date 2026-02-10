/**
 * https://leetcode.com/problems/basic-calculator/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "224. Basic Calculator"
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
 * Преобразует целое число в английские слова.
 * 
 * @param {number} num - Число от 0 до 2^31-1
 * @return {string} Словесное представление с заглавной буквы
 * 
 * @example
 * // Возвращает "One Hundred Twenty Three"
 * numberToWords(123)
 * @example
 * // Возвращает "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
 * numberToWords(1234567)
 * 
 * Особенности реализации:
 *   - Обрабатывает сложные случаи: 1000010 → "One Million Ten"
 *   - Удаляет лишние пробелы
 */
var numberToWords = function(num) {
    if (num === 0) return "Zero";
    
    const ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", 
                 "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", 
                 "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"];
    const tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", 
                 "Sixty", "Seventy", "Eighty", "Ninety"];
    const thousands = ["", "Thousand", "Million", "Billion"];
    
    const helper = (n) => {
        if (n === 0) return "";
        if (n < 20) return ones[n] + " ";
        if (n < 100) return tens[Math.floor(n / 10)] + " " + helper(n % 10);
        return ones[Math.floor(n / 100)] + " Hundred " + helper(n % 100);
    };
    
    let result = "";
    let i = 0;
    
    while (num > 0) {
        if (num % 1000 !== 0) {
            result = helper(num % 1000).trim() + " " + thousands[i] + " " + result;
        }
        num = Math.floor(num / 1000);
        i++;
    }
    
    return result.trim();
};