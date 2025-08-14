/**
 * https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/
 */

/**
 * Находит максимальную прибыль от одной покупки и одной продажи акции.
 * 
 * Алгоритм:
 * - Проходим по массиву цен.
 * - Для каждой цены обновляем минимальную цену и максимальную прибыль.
 *
 * Время: O(n), Память: O(1)
 * 
 * @param {number[]} prices - Массив цен акций.
 * @return {number} Максимальная прибыль.
 */
var maxProfit = function(prices) {
    let minPrice = Infinity;
    let maxProfit = 0;
    for (let price of prices) {
        minPrice = Math.min(minPrice, price);
        maxProfit = Math.max(maxProfit, price - minPrice);
    }
    return maxProfit;
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/