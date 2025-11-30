/**
 * https://leetcode.com/problems/permutations-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Permutations II" на C#
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
    public IList<IList<int>> PermuteUnique(int[] nums) {
        var result = new List<IList<int>>();
        Array.Sort(nums);
        var used = new bool[nums.Length];
        Backtrack(nums, used, new List<int>(), result);
        return result;
    }
    
    private void Backtrack(int[] nums, bool[] used, List<int> current, List<IList<int>> result) {
        if (current.Count == nums.Length) {
            result.Add(new List<int>(current));
            return;
        }
        
        for (int i = 0; i < nums.Length; i++) {
            if (used[i]) continue;
            if (i > 0 && nums[i] == nums[i-1] && !used[i-1]) continue;
            
            used[i] = true;
            current.Add(nums[i]);
            Backtrack(nums, used, current, result);
            current.RemoveAt(current.Count - 1);
            used[i] = false;
        }
    }
}