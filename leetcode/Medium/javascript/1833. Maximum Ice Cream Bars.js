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
 * Находит максимальное количество мороженого, которое можно купить.
 * 
 * Использует жадный подход: сортирует цены по возрастанию и покупает
 * самое дешевое мороженое, пока хватает монет.
 *
 * @param {number[]} costs - массив цен на различные виды мороженого
 * @param {number} coins - количество доступных монет (бюджет)
 * @returns {number} максимальное количество видов мороженого, которое можно купить
 *
 * @example
 * maxIceCream([1,3,2,4,1], 7) // => 4
 * maxIceCream([10,6,8,7,7,8], 5) // => 0
 * maxIceCream([1,6,3,1,2,5], 20) // => 6
 */
function maxIceCream(costs, coins) {
    // Сортируем цены по возрастанию для жадного выбора
    costs.sort((a, b) => a - b);
    
    let count = 0;
    let totalCost = 0;
    
    // Покупаем мороженое, пока хватает монет
    for (let cost of costs) {
        if (totalCost + cost <= coins) {
            totalCost += cost;
            count++;
        } else {
            break;
        }
    }
    
    return count;
}

// Альтернативное решение с использованием reduce
/**
 * Альтернативная реализация с использованием reduce.
 * 
 * @param {number[]} costs - массив цен на мороженое
 * @param {number} coins - доступный бюджет
 * @returns {number} количество купленного мороженого
 */
function maxIceCreamReduce(costs, coins) {
    costs.sort((a, b) => a - b);
    
    let spent = 0;
    return costs.reduce((count, cost) => {
        spent += cost;
        return spent <= coins ? count + 1 : count;
    }, 0);
}

// Экспорт для использования в модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { maxIceCream, maxIceCreamReduce };
}