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
 * @param {number[]} nums
 * @return {string}
 */
var largestNumber = function(nums) {
    // Преобразуем в строки
    const strNums = nums.map(num => num.toString());
    
    // Сортируем с кастомным компаратором
    strNums.sort((a, b) => {
        const order1 = a + b;
        const order2 = b + a;
        return order2.localeCompare(order1); // Обратный порядок
    });
    
    // Если первый элемент "0", возвращаем "0"
    if (strNums[0] === '0') {
        return '0';
    }
    
    // Собираем результат
    return strNums.join('');
};