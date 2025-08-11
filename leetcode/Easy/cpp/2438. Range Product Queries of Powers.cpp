/**
 * https://leetcode.com/problems/range-product-queries-of-powers/description/?envType=daily-question&envId=2025-08-11
 */

/*
 * Функция productQueries:
 * @param n — исходное число, разбивается на степени двойки.
 * @param queries — вектор запросов [l, r].
 * @return вектор ответов — произведения степеней двойки в диапазоне по модулю 1e9+7.
 *
 * Подход:
 * 1. Извлекаем set-биты n, формируя массив степеней двойки.
 * 2. Строим префиксный массив накопленных произведений mod.
 * 3. Для запроса используем modular inverse (быстрое возведение в степень).
 */
class Solution {
public:
    vector<int> productQueries(int n, vector<vector<int>>& queries) {
        const int MOD = 1e9 + 7;
        vector<long long> powers;
        for (int i = 0; i < 31; ++i) {
            if (n & (1 << i)) {
                powers.push_back(1LL << i);
            }
        }
        int m = powers.size();
        vector<long long> pre(m + 1, 1);
        for (int i = 0; i < m; ++i) {
            pre[i + 1] = pre[i] * powers[i] % MOD;
        }

        vector<int> ans;
        for (auto& q : queries) {
            int l = q[0], r = q[1];
            long long prod = pre[r + 1] * modPow(pre[l], MOD - 2, MOD) % MOD;
            ans.push_back((int)prod);
        }
        return ans;
    }

private:
    long long modPow(long long a, long long b, int mod) {
        long long res = 1;
        a %= mod;
        while (b > 0) {
            if (b & 1) res = res * a % mod;
            a = a * a % mod;
            b >>= 1;
        }
        return res;
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
