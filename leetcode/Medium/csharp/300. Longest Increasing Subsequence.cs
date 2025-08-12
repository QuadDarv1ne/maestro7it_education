/**
 * https://leetcode.com/problems/longest-increasing-subsequence/description/?envType=study-plan-v2&envId=top-interview-150
 */

using System;
using System.Collections.Generic;

public class Solution {
    public int LengthOfLIS(int[] nums) {
        /**
         * Находит длину самой длинной строго возрастающей подпоследовательности в массиве nums.
         * Использует двоичный поиск для эффективного решения задачи за O(n log n).
         *
         * @param nums: Массив целых чисел.
         * @return: Длина самой длинной возрастающей подпоследовательности.
         */
        List<int> tails = new List<int>();
        foreach (int num in nums) {
            int idx = tails.BinarySearch(num);
            if (idx < 0) idx = ~idx;
            if (idx == tails.Count) {
                tails.Add(num);
            } else {
                tails[idx] = num;
            }
        }
        return tails.Count;
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