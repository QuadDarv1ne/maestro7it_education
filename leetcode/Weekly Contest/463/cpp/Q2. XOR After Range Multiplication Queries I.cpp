/**
 * Решение задачи "XOR After Range Multiplication Queries I"
 * 
 * Задача: https://leetcode.com/contest/weekly-contest-463/problems/xor-after-range-multiplication-queries-i/
 * 
 * Описание:
 * Дано:
 * - массив чисел `nums`,
 * - массив запросов `queries`, каждый запрос состоит из четырех целых чисел [l, r, k, v].
 * 
 * Для каждого запроса:
 * 1. Проходим по подотрезку nums[l..r] с шагом k.
 * 2. Умножаем каждый элемент подотрезка на v и берём результат по модулю MOD = 10^9 + 7.
 * 
 * После выполнения всех запросов необходимо вернуть XOR всех элементов массива `nums`.
 * 
 * Алгоритм:
 * 1. Обрабатываем каждый запрос поочередно.
 * 2. Для каждого индекса подотрезка применяем операцию умножения с модулем.
 * 3. После всех запросов вычисляем XOR всех элементов массива.
 *
 * Временная сложность: O(Q * ((R-L)/K)), где Q — количество запросов, 
 * R-L — длина подотрезка, K — шаг.
 * Пространственная сложность: O(1) дополнительной памяти.
 *
 * Пример использования:
 * vector<int> nums = {1, 2, 3};
 * vector<vector<int>> queries = {{0, 2, 1, 2}};
 * Solution sol;
 * int result = sol.xorAfterQueries(nums, queries);
 * 
 * @param nums — вектор чисел.
 * @param queries — вектор запросов, каждый запрос [l, r, k, v].
 * @return Результат XOR после всех операций.
 */

#define LL long long
#define VECI vector<int>
#define VECVI vector<vector<int>>
#define MOD 1000000007
#define FOR_EACH_Q(q, queries) for (const auto& q : queries)
#define FOR_STEP(i, l, r, k) for (int i = (l); i <= (r); i += (k))

class Solution {
public:
    int xorAfterQueries(vector<int>& nums, vector<vector<int>>& queries) {
        FOR_EACH_Q(q, queries) {
        int l = q[0];
        int r = q[1];
        int k = q[2];
        int v = q[3];
        FOR_STEP(idx, l, r, k) {
            nums[idx] = (int)(((LL)nums[idx] * v) % MOD);
        }
    }

    int xorSum = 0;
    for (int num : nums) {
        xorSum ^= num;
    }

    return xorSum;
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