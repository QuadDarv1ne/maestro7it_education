/**
 * https://leetcode.com/contest/weekly-contest-463/problems/best-time-to-buy-and-sell-stock-using-strategy/
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