/**
 * https://leetcode.com/problems/kth-largest-element-in-an-array/description/
 */

using System;
using System.Collections.Generic;

public class Solution {
    public int FindKthLargest(int[] nums, int k) {
        /**
         * Находит k-й по величине элемент с помощью min-heap.
         * Время: O(n log k), память: O(k)
         */
        SortedSet<(int val, int idx)> heap = new SortedSet<(int, int)>();
        int idx = 0;
        foreach (var num in nums) {
            heap.Add((num, idx++));
            if (heap.Count > k) heap.Remove(heap.Min);
        }
        return heap.Min.val;
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