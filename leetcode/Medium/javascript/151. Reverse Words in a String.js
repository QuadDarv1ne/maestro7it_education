/**
 * https://leetcode.com/problems/reverse-words-in-a-string/description/
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
 * Разворачивает порядок слов в строке
 * 
 * @param {string} s - Исходная строка с возможными лишними пробелами
 * @return {string} Строка с обратным порядком слов, разделенных одним пробелом
 * 
 * Алгоритм:
 * - Обрабатываем строку с конца к началу
 * - Используем два указателя для нахождения границ слов
 * - Собираем слова в результирующую строку
 */
var reverseWords = function(s) {
    let result = [];
    let i = s.length - 1;
    
    while (i >= 0) {
        // Пропускаем пробелы с конца
        while (i >= 0 && s[i] === ' ') {
            i--;
        }
        
        if (i < 0) {
            break;
        }
        
        let j = i;
        // Находим начало слова
        while (j >= 0 && s[j] !== ' ') {
            j--;
        }
        
        // Извлекаем слово и добавляем в результат
        result.push(s.substring(j + 1, i + 1));
        
        // Переходим к следующему слову
        i = j - 1;
    }
    
    return result.join(' ');
};