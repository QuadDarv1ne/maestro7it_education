/**
 * https://leetcode.com/problems/coin-change/description/?envType=study-plan-v2&envId=top-interview-150
 */

using System;

public class Solution {
    /// <summary>
    /// Найти минимальное количество монет для набора суммы amount.
    /// Если сумму невозможно составить, вернуть -1.
    /// </summary>
    /// <param name="coins">Массив номиналов монет</param>
    /// <param name="amount">Целевая сумма</param>
    /// <returns>Минимальное количество монет или -1</returns>
    public int CoinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Array.Fill(dp, amount + 1);
        dp[0] = 0;

        foreach (int coin in coins) {
            for (int x = coin; x <= amount; x++) {
                dp[x] = Math.Min(dp[x], dp[x - coin] + 1);
            }
        }

        return dp[amount] > amount ? -1 : dp[amount];
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