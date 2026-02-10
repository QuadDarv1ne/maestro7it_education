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
 * Definition for isBadVersion()
 * 
 * @param {integer} version number
 * @return {boolean} whether the version is bad
 * isBadVersion = function(version) {
 *     ...
 * };
 */

/**
 * @param {function} isBadVersion()
 * @return {function}
 */
var solution = function(isBadVersion) {
    /**
     * Находит первую плохую версию с помощью бинарного поиска.
     * 
     * @param {number} n - Количество версий (от 1 до n)
     * @return {number} Первая версия, которая является плохой
     * 
     * @example
     * // Возвращает 4
     * firstBadVersion(5)
     * 
     * Сложность:
     *   Время: O(log n)
     *   Память: O(1)
     */
    return function(n) {
        let left = 1, right = n;
        
        while (left < right) {
            // Избегаем переполнения
            const mid = Math.floor(left + (right - left) / 2);
            
            if (isBadVersion(mid)) {
                // mid может быть первой плохой версией
                right = mid;
            } else {
                // Первая плохая версия справа от mid
                left = mid + 1;
            }
        }
        
        return left;  // left == right
    };
};