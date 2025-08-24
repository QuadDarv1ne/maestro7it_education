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
 * Найти минимальную возможную сумму элементов массива после того, как мы можем удалить
 * несколько подотрезков с суммой, кратной `k`.
 *
 * Алгоритм:
 * 1. Используем префиксные суммы `p_sum`.
 * 2. Храним минимальную сумму для каждого остатка по модулю `k` в `min_sum_for_rem`.
 * 3. Для каждого числа:
 *    - обновляем текущую префиксную сумму,
 *    - вычисляем остаток по модулю `k`,
 *    - обновляем минимальную возможную сумму с учётом уже встречавшихся остатков.
 * 4. В конце возвращаем минимальную возможную сумму.
 *
 * Временная сложность: O(n), где n — длина массива `nums`.
 * Пространственная сложность: O(k) для хранения остатков.
 *
 * Пример использования:
 * vector<int> nums = {3, 7, 2, 5};
 * int k = 3;
 * Solution sol;
 * long long result = sol.minArraySum(nums, k);
 * 
 * @param nums — вектор чисел.
 * @param k — число, по которому проверяется делимость суммы удаляемых подотрезков.
 * @return Минимальная возможная сумма массива после удаления подотрезков.
 */

#define LL long long
#define VI vector<int>
#define UMII unordered_map<int, LL>
#define MIN(a, b) ((a) < (b) ? (a) : (b))

class Solution {
public:
    long long minArraySum(vector<int>& nums, int k) {
        UMII min_sum_for_rem;
    min_sum_for_rem[0] = 0;

    LL p_sum = 0;
    LL min_sum = 0;

    for (int num : nums) {
        p_sum += num;
        int rem = (int)((p_sum % k + k) % k);

        LL next_min_sum = min_sum + num;

        if (min_sum_for_rem.count(rem)) {
            next_min_sum = MIN(next_min_sum, min_sum_for_rem[rem]);
        }
        
        min_sum = next_min_sum;

        if (!min_sum_for_rem.count(rem) || min_sum < min_sum_for_rem[rem]) {
            min_sum_for_rem[rem] = min_sum;
        }
    }

    return min_sum;
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