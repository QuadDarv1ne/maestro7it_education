/**
 * https://leetcode.com/problems/ways-to-express-an-integer-as-sum-of-powers/description/?envType=daily-question&envId=2025-08-12
 */

#include <vector>

/**
 * Задача: Найти количество способов представить число n как сумму уникальных целых чисел,
 * возведённых в степень x.
 * 
 * Решение использует динамическое программирование с мемоизацией и рекурсивный обход.
 */

const int MOD = 1e9 + 7;

/**
 * Целочисленное возведение в степень.
 * 
 * @param base - основание степени.
 * @param exp - показатель степени.
 * @return Результат base^exp типа long long.
 */
long long intPow(int base, int exp) {
    long long result = 1;
    for (int i = 0; i < exp; ++i) {
        result *= base;
    }
    return result;
}

class Solution {
public:
    /**
     * Основная функция для вычисления количества способов представить n как сумму степеней.
     * 
     * @param n - число, которое нужно представить.
     * @param x - степень, в которую возводятся числа.
     * @return Количество способов по модулю 10^9+7.
     */
    int numberOfWays(int n, int x) {
        // Вычисляем максимальное основание, для которого i^x <= n
        int maxBase = 1;
        while (intPow(maxBase + 1, x) <= n) {
            maxBase++;
        }
        // dp[i][remaining] - количество способов представить remaining с использованием чисел до i
        std::vector<std::vector<int>> dp(maxBase + 1, std::vector<int>(n + 1, -1));
        return dfs(maxBase, n, x, dp);
    }

private:
    /**
     * Рекурсивная функция с мемоизацией для подсчёта количества способов.
     * 
     * @param i - текущее максимальное число для использования.
     * @param remaining - оставшаяся сумма, которую нужно представить.
     * @param x - степень.
     * @param dp - мемоизация результатов.
     * @return Количество способов представить remaining с числами <= i.
     */
    int dfs(int i, int remaining, int x, std::vector<std::vector<int>>& dp) {
        if (remaining == 0) return 1;       // Нашли способ
        if (i == 0 || remaining < 0) return 0; // Нет способа
        if (dp[i][remaining] != -1) return dp[i][remaining]; // Используем сохранённый результат

        long long power = intPow(i, x);
        int include = 0;
        if (power <= remaining) {
            include = dfs(i - 1, remaining - power, x, dp);
        }
        int exclude = dfs(i - 1, remaining, x, dp);

        dp[i][remaining] = (include + exclude) % MOD;
        return dp[i][remaining];
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