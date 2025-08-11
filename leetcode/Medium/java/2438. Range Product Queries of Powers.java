/**
 * https://leetcode.com/problems/range-product-queries-of-powers/?envType=daily-question&envId=2025-08-11
 */

/**
 * Метод productQueries:
 * @param n — входное положительное целое число, представлено как сумма степеней двойки.
 * @param queries — список запросов вида [l, r]; нужно вычислить произведение powers[l..r] mod 1e9+7.
 * @return массив ответов по каждому запросу.
 *
 * Идея решения:
 * 1. Собираем все степени двойки (set-bits) из n.
 * 2. Строим префиксный массив произведений mod.
 * 3. Для каждого запроса вычисляем произведение через деление на префиксный элемент (используется модульная инверсия).
 */
class Solution {
    private static final int MOD = (int)1e9 + 7;

    public int[] productQueries(int n, int[][] queries) {
        List<Integer> powers = new ArrayList<>();
        for (int i = 0; i < 31; i++) {
            if ((n & (1 << i)) != 0) {
                powers.add(1 << i);
            }
        }
        int m = powers.size();
        long[] pre = new long[m + 1];
        pre[0] = 1;
        for (int i = 0; i < m; i++) {
            pre[i + 1] = pre[i] * powers.get(i) % MOD;
        }

        int[] ans = new int[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int l = queries[i][0], r = queries[i][1];
            long prod = pre[r + 1] * modPow(pre[l], MOD - 2) % MOD;
            ans[i] = (int) prod;
        }
        return ans;
    }

    // Быстрое возведение в степень по модулю для вычисления обратного по модулю
    private long modPow(long a, long b) {
        long res = 1;
        a %= MOD;
        while (b > 0) {
            if ((b & 1) == 1) {
                res = res * a % MOD;
            }
            a = a * a % MOD;
            b >>= 1;
        }
        return res;
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
