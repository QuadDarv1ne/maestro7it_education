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
 * @param {number} k
 * @param {number[]} prices
 * @return {number}
 * 
 * Найти максимальную прибыль от транзакций с акциями при ограничении на количество транзакций.
 * 
 * @param {number} k Максимальное количество разрешенных транзакций
 * @param {number[]} prices Массив цен акций по дням
 * @return {number} Максимальная прибыль
 * 
 * Алгоритм:
 * 1. Если k >= n/2, используется алгоритм для неограниченного числа транзакций.
 * 2. Иначе используется динамическое программирование с двумя массивами.
 * 
 * Пример:
 * maxProfit(2, [3,2,6,5,0,3]) // возвращает 7
 */
var maxProfit = function(k, prices) {
    const n = prices.length;
    if (n <= 1 || k === 0) return 0;
    
    // Если k достаточно большое
    if (k >= Math.floor(n / 2)) {
        let profit = 0;
        for (let i = 1; i < n; i++) {
            if (prices[i] > prices[i-1]) {
                profit += prices[i] - prices[i-1];
            }
        }
        return profit;
    }
    
    // Динамическое программирование
    const buy = new Array(k + 1).fill(-Infinity);
    const sell = new Array(k + 1).fill(0);
    
    for (const price of prices) {
        for (let i = k; i >= 1; i--) {
            buy[i] = Math.max(buy[i], sell[i-1] - price);
            sell[i] = Math.max(sell[i], buy[i] + price);
        }
    }
    
    return sell[k];
};