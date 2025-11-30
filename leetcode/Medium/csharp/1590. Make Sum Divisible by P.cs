/**
 * https://leetcode.com/problems/make-sum-divisible-by-p/description/?envType=daily-question&envId=2025-11-30
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Make Sum Divisible by P" на C#
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

using System;
using System.Collections.Generic;

public class Solution {
    public int MinSubarray(int[] nums, int p) {
        long totalSum = 0;
        foreach (int num in nums) totalSum += num;
        int remainder = (int)(totalSum % p);
        if (remainder == 0) return 0;

        Dictionary<int, int> prefixMap = new Dictionary<int, int>();
        prefixMap.Add(0, -1);
        int prefixSum = 0;
        int minLength = nums.Length;

        for (int i = 0; i < nums.Length; i++) {
            prefixSum = (prefixSum + nums[i]) % p;
            int target = (prefixSum - remainder + p) % p;
            if (prefixMap.ContainsKey(target)) {
                minLength = Math.Min(minLength, i - prefixMap[target]);
            }
            prefixMap[prefixSum] = i;
        }
        return minLength < nums.Length ? minLength : -1;
    }
}