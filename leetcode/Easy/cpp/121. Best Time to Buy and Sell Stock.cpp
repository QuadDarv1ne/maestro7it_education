/**
 * https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/
 */

#include <vector>
#include <algorithm>

/**
 * @brief Находит максимальную прибыль от одной покупки и одной продажи акции.
 *
 * Алгоритм:
 * - Проходим по массиву цен.
 * - Для каждой цены обновляем минимальную цену и максимальную прибыль.
 *
 * Время: O(n), Память: O(1)
 */
class Solution {
public:
    int maxProfit(std::vector<int>& prices) {
        int min_price = INT_MAX;
        int max_profit = 0;
        for (int price : prices) {
            min_price = std::min(min_price, price);
            max_profit = std::max(max_profit, price - min_price);
        }
        return max_profit;
    }
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