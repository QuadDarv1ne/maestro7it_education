/**
 * https://leetcode.com/problems/coin-change/description/?envType=study-plan-v2&envId=top-interview-150
 */

/**
 * Найти минимальное количество монет для набора суммы amount.
 * Если сумму невозможно составить, вернуть -1.
 *
 * @param {number[]} coins - массив номиналов монет
 * @param {number} amount - целевая сумма
 * @return {number} минимальное количество монет или -1
 *
 * Алгоритм:
 * Используем динамическое программирование:
 * dp[x] = минимальное количество монет для суммы x
 * dp[0] = 0
 * Для каждого coin обновляем dp[x], начиная с coin до amount
 *
 * Время: O(n * amount), где n = количество монет
 * Память: O(amount)
 */
var coinChange = function(coins, amount) {
    const dp = new Array(amount + 1).fill(amount + 1);
    dp[0] = 0;

    for (let coin of coins) {
        for (let x = coin; x <= amount; x++) {
            dp[x] = Math.min(dp[x], dp[x - coin] + 1);
        }
    }

    return dp[amount] > amount ? -1 : dp[amount];
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