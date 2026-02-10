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
 * Находит h-индекс из отсортированного массива цитирований.
 * 
 * H-индекс: максимальное число h, такое что имеется как минимум h статей,
 * каждая из которых цитируется как минимум h раз.
 * 
 * @param {number[]} citations - Отсортированный массив цитирований (по возрастанию)
 * @return {number} h-индекс
 * 
 * @example
 * // Возвращает 3
 * hIndex([0,1,3,5,6])
 * @example
 * // Возвращает 2
 * hIndex([1,2,100])
 * 
 * Сложность:
 *   Время: O(log n)
 *   Память: O(1)
 */
var hIndex = function(citations) {
    const n = citations.length;
    let left = 0, right = n - 1;
    
    while (left <= right) {
        const mid = Math.floor(left + (right - left) / 2);
        const papers = n - mid;  // Количество статей с цитированиями >= citations[mid]
        
        if (citations[mid] >= papers) {
            // Ищем в левой части для большего h
            right = mid - 1;
        } else {
            // Ищем в правой части
            left = mid + 1;
        }
    }
    
    return n - left;
};