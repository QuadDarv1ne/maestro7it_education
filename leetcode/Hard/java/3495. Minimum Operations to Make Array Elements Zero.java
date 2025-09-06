/**
 * https://leetcode.com/problems/minimum-operations-to-make-array-elements-zero/description/?envType=daily-question&envId=2025-09-06
 */

class Solution {
    /**
     * Задача: Для каждого диапазона [l, r] вычислить минимальное количество операций,
     * чтобы все элементы массива стали равны нулю.
     * Операция: выбрать два числа и заменить их на floor(a/4) и floor(b/4).
     * Итоговый результат — сумма по всем запросам.
     */
    public long minOperations(int[][] queries) {
        long ans = 0;
        for (int[] q : queries) {
            int l = q[0], r = q[1];
            ans += (getOps(r) - getOps(l - 1) + 1) / 2;
        }
        return ans;
    }

    private long getOps(int n) {
        long res = 0;
        long ops = 0;
        long pw = 1;
        while (pw <= n) {
            long l = pw;
            long r = Math.min(n, pw * 4 - 1);
            ops++;
            res += (r - l + 1) * ops;
            pw *= 4;
        }
        return res;
    }
}

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