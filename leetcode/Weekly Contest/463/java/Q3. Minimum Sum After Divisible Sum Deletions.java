/**
 * Решение задачи "Minimum Sum After Divisible Sum Deletions"
 * 
 * Задача: https://leetcode.com/contest/weekly-contest-463/problems/minimum-sum-after-divisible-sum-deletions/
 * 
 * Описание:
 * Дано:
 * - массив чисел `nums`,
 * - целое число `k`.
 * 
 * Задача:
 * Найти минимальную возможную сумму элементов массива после того, как можно удалить
 * несколько подотрезков с суммой, кратной `k`.
 *
 * Алгоритм:
 * 1. Используем динамическое программирование с массивом `dp` длины k, где dp[rem] хранит
 *    максимальную разницу между суммой подотрезков и префиксной суммой для остатка rem по модулю k.
 * 2. Проходим по массиву `nums`, накапливаем префиксную сумму `sum`.
 * 3. Для текущего остатка `sum % k` обновляем максимальную возможную удалённую сумму `max`.
 * 4. Обновляем dp[rem] для текущего остатка.
 * 5. В конце возвращаем минимальную сумму: total_sum - max.
 *
 * Временная сложность: O(n), где n — длина массива `nums`.
 * Пространственная сложность: O(k) для хранения массива dp.
 *
 * Пример использования:
 * int[] nums = {3, 7, 2, 5};
 * int k = 3;
 * Solution sol = new Solution();
 * long result = sol.minArraySum(nums, k);
 * 
 * @param nums — массив чисел.
 * @param k — число, по которому проверяется делимость суммы удаляемых подотрезков.
 * @return Минимальная возможная сумма массива после удаления подотрезков.
 */

class Solution {
    public long minArraySum(int[] nums, int k) {
        long dp[] = new long[k], sum = 0, max = 0;
        for (int i = 1; i < k; i++) {
            dp[i] = Long.MIN_VALUE;
        }
        for (int num : nums) {
            sum += num;
            max = Math.max(max, dp[(int) (sum % k)] + sum);
            dp[(int) (sum % k)] = Math.max(dp[(int) (sum % k)], max - sum);
        }
        return sum - max;
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