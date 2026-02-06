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

var convertToTitle = function(columnNumber) {
    /**
     * Преобразует номер столбца в заголовок столбца Excel.
     * Это преобразование из системы по основанию 10 в систему по основанию 26.
     * 
     * Сложность по времени: O(log₂₆(n))
     * Сложность по памяти: O(log₂₆(n))
     */
    let result = '';
    
    while (columnNumber > 0) {
        // Уменьшаем на 1 для корректного маппинга (1->A, не 0->A)
        columnNumber--;
        
        // Получаем остаток и преобразуем в букву
        const remainder = columnNumber % 26;
        result = String.fromCharCode('A'.charCodeAt(0) + remainder) + result;
        
        // Переходим к следующему разряду
        columnNumber = Math.floor(columnNumber / 26);
    }
    
    return result;
};