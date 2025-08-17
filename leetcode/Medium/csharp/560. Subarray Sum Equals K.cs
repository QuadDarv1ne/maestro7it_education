/**
 * https://leetcode.com/problems/subarray-sum-equals-k/description/
 */

using System;
using System.Collections.Generic;

public class Solution {
    public int SubarraySum(int[] nums, int k) {
        /**
         * Задача: найти количество подмассивов, сумма которых равна k.
         *
         * Алгоритм:
         * - Используем префиксные суммы и словарь Dictionary<int, int>.
         * - Для каждого элемента проверяем, встречался ли prefixSum - k.
         *
         * Сложность:
         * - Время: O(n)
         * - Память: O(n)
         */
        var prefixCounts = new Dictionary<int, int>();
        prefixCounts[0] = 1;

        int currentSum = 0, count = 0;
        foreach (int num in nums) {
            currentSum += num;
            if (prefixCounts.ContainsKey(currentSum - k))
                count += prefixCounts[currentSum - k];
            if (!prefixCounts.ContainsKey(currentSum))
                prefixCounts[currentSum] = 0;
            prefixCounts[currentSum]++;
        }
        return count;
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