/**
 * https://leetcode.com/problems/minimum-operations-to-make-array-elements-zero/description/?envType=daily-question&envId=2025-09-06
 */

/**
 * Задача: Для каждого запроса [l, r] посчитать минимальное число операций,
 * чтобы все элементы диапазона стали равны нулю.
 * Операция: два числа a и b заменяются на floor(a/4) и floor(b/4).
 * Возвращается сумма по всем запросам.
 *
 * @param {number[][]} queries
 * @return {number}
 */
var minOperations = function(queries) {
    let ans = 0;
    const getOps = (n) => {
        let res = 0, ops = 0;
        for (let pw = 1; pw <= n; pw *= 4) {
            ops++;
            let l = pw;
            let r = Math.min(n, pw * 4 - 1);
            res += (r - l + 1) * ops;
        }
        return res;
    };

    for (const q of queries) {
        const [l, r] = q;
        ans += Math.floor((getOps(r) - getOps(l - 1) + 1) / 2);
    }
    return ans;
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