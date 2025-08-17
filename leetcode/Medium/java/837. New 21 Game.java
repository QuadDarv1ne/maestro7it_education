/**
 * https://leetcode.com/problems/new-21-game/description/?envType=daily-question&envId=2025-08-17
 */

class Solution {
    /**
     * Игра "Новый Блэкджек".
     * Мы начинаем с 0 очков и тянем карты до тех пор, пока сумма < k.
     * Каждая карта даёт от 1 до maxPts очков равновероятно.
     * Нужно вычислить вероятность того, что итоговая сумма ≤ n.
     *
     * @param n максимальное количество очков, которое нас устраивает
     * @param k порог остановки (перестаём тянуть карты, если сумма >= k)
     * @param maxPts максимальное количество очков за карту
     * @return вероятность, что итоговое количество очков ≤ n
     */
    public double new21Game(int n, int k, int maxPts) {
        if (k == 0 || n >= k - 1 + maxPts) return 1.0;

        double[] dp = new double[n + 1];
        dp[0] = 1.0;
        double windowSum = 1.0, result = 0.0;

        for (int i = 1; i <= n; i++) {
            dp[i] = windowSum / maxPts;
            if (i < k) {
                windowSum += dp[i];
            } else {
                result += dp[i];
            }
            if (i - maxPts >= 0) {
                windowSum -= dp[i - maxPts];
            }
        }
        return result;
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