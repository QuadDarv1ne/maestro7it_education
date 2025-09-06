/**
 * https://leetcode.com/problems/minimum-operations-to-make-array-elements-zero/description/?envType=daily-question&envId=2025-09-06
 */

class Solution {
public:
    /**
     * Задача: Для каждого запроса [l, r] вычислить минимальное количество операций,
     * необходимых, чтобы все элементы массива из диапазона [l..r] стали равны нулю.
     * Операция: заменить числа a и b на floor(a/4) и floor(b/4).
     * Возвращается сумма по всем запросам.
     */
    long long minOperations(vector<vector<int>>& queries) {
        long long ans = 0;
        for (auto &q : queries) {
            int l = q[0], r = q[1];
            ans += (getOps(r) - getOps(l - 1) + 1) / 2;
        }
        return ans;
    }

private:
    long long getOps(int n) {
        long long res = 0;
        int ops = 0;
        for (long long pw = 1; pw <= n; pw *= 4) {
            long long l = pw;
            long long r = min<long long>(n, pw * 4 - 1);
            ops++;
            res += (r - l + 1) * ops;
        }
        return res;
    }
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/