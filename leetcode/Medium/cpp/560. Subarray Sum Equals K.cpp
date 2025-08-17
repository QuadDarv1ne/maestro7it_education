/**
 * https://leetcode.com/problems/subarray-sum-equals-k/description/
 */

#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        /**
         * Задача: найти количество подмассивов, сумма которых равна k.
         *
         * Алгоритм:
         * 1. Используем префиксные суммы.
         * 2. unordered_map хранит количество вхождений каждой суммы.
         * 3. Для каждого элемента проверяем, встречался ли prefix_sum - k.
         * 4. Если да — увеличиваем счётчик.
         *
         * Сложность:
         * - Время: O(n)
         * - Память: O(n)
         */
        unordered_map<int, int> prefixCounts;
        prefixCounts[0] = 1;

        int currentSum = 0, count = 0;
        for (int num : nums) {
            currentSum += num;
            if (prefixCounts.count(currentSum - k))
                count += prefixCounts[currentSum - k];
            prefixCounts[currentSum]++;
        }
        return count;
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