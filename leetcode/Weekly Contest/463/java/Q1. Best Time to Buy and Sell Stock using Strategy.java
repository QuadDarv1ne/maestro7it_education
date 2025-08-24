/**
 * Решение задачи "Best Time to Buy and Sell Stock Using Strategy"
 * 
 * Задача: https://leetcode.com/contest/weekly-contest-463/problems/best-time-to-buy-and-sell-stock-using-strategy/
 * 
 * Описание:
 * Дано:
 * - массив `prices`, где prices[i] — цена акции в день i,
 * - массив `strategy`, где strategy[i] = 0 или 1,
 * - целое число `k`, длина подотрезка, на котором можно изменить стратегию.
 *
 * Задача:
 * Найти максимальную прибыль, которую можно получить, изменяя стратегию на подотрезке длины k.
 * 
 * Алгоритм:
 * 1. Вычисляем префиксные суммы цен `sum` и сумм по стратегии `dp`.
 * 2. Скользящим окном длины k проходим по массиву и вычисляем потенциальный прирост прибыли.
 * 3. Обновляем максимальное значение прироста `max`.
 * 4. Возвращаем сумму исходной прибыли и максимального прироста.
 *
 * Временная сложность: O(n), где n — длина массива `prices`.
 * Пространственная сложность: O(n) для хранения префиксных сумм.
 *
 * Пример использования:
 * int[] prices = {3, 2, 5, 1};
 * int[] strategy = {0, 1, 0, 1};
 * int k = 2;
 * Solution sol = new Solution();
 * long result = sol.maxProfit(prices, strategy, k);
 * 
 * @param prices — массив цен акций.
 * @param strategy — массив стратегии (0 или 1).
 * @param k — длина подотрезка для изменения стратегии.
 * @return Максимальная возможная прибыль.
 */

class Solution {
    public long maxProfit(int[] prices, int[] strategy, int k) {
        long sum[] = new long[prices.length + 1], dp[] = new long[prices.length + 1], max = 0;
        for (int i = 0; i < prices.length; i++) {
            sum[i + 1] = sum[i] + prices[i];
            dp[i + 1] = dp[i] + strategy[i] * prices[i];
        }
        for (int i = k; i <= prices.length; i++) {
            max = Math.max(max, sum[i] - sum[i - k / 2] - dp[i] + dp[i - k]);
        }
        return max + dp[prices.length];
    }
}

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