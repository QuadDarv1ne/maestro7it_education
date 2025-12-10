/* ========================== C# ========================== */

/*
 * LeetCode 78: Subsets (Подмножества)
 * https://leetcode.com/problems/subsets/
 * 
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Описание задачи:
 * Дан массив уникальных целых чисел nums. Вернуть все возможные подмножества
 * (множество степени / power set). Решение не должно содержать дубликаты.
 * 
 * Примеры:
 * Input: nums = [1,2,3]
 * Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
 * 
 * Input: nums = [0]
 * Output: [[],[0]]
 * 
 * Ограничения:
 * - 1 <= nums.length <= 10
 * - -10 <= nums[i] <= 10
 * - Все числа в nums уникальны
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. YouTube канал: https://www.youtube.com/@it-coders
 * 6. ВК группа: https://vk.com/science_geeks
 */
 
using System;
using System.Collections.Generic;

public class Solution {
    // ========== ПОДХОД 1: Backtracking ==========
    public IList<IList<int>> Subsets(int[] nums) {
        IList<IList<int>> result = new List<IList<int>>();
        Backtrack(nums, 0, new List<int>(), result);
        return result;
    }
    
    private void Backtrack(int[] nums, int index, 
                          List<int> path, IList<IList<int>> result) {
        // Каждый путь - валидное подмножество
        result.Add(new List<int>(path));
        
        // Пробуем добавить оставшиеся элементы
        for (int i = index; i < nums.Length; i++) {
            path.Add(nums[i]);
            Backtrack(nums, i + 1, path, result);
            path.RemoveAt(path.Count - 1);
        }
    }
    
    // ========== ПОДХОД 2: Итеративный ==========
    public IList<IList<int>> SubsetsIterative(int[] nums) {
        IList<IList<int>> result = new List<IList<int>>();
        result.Add(new List<int>());  // Пустое подмножество
        
        foreach (int num in nums) {
            int size = result.Count;
            for (int i = 0; i < size; i++) {
                List<int> newSubset = new List<int>(result[i]);
                newSubset.Add(num);
                result.Add(newSubset);
            }
        }
        
        return result;
    }
    
    // ========== ПОДХОД 3: Битовые маски ==========
    public IList<IList<int>> SubsetsBitmask(int[] nums) {
        IList<IList<int>> result = new List<IList<int>>();
        int n = nums.Length;
        
        for (int mask = 0; mask < (1 << n); mask++) {
            List<int> subset = new List<int>();
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) != 0) {
                    subset.Add(nums[i]);
                }
            }
            result.Add(subset);
        }
        
        return result;
    }
}