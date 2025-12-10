/* ========================== JAVA ========================== */

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

import java.util.*;

class Solution {
    // ========== ПОДХОД 1: Backtracking ==========
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(nums, 0, new ArrayList<>(), result);
        return result;
    }
    
    private void backtrack(int[] nums, int index, 
                          List<Integer> path, List<List<Integer>> result) {
        // Каждый путь - валидное подмножество
        result.add(new ArrayList<>(path));
        
        // Пробуем добавить оставшиеся элементы
        for (int i = index; i < nums.length; i++) {
            path.add(nums[i]);
            backtrack(nums, i + 1, path, result);
            path.remove(path.size() - 1);
        }
    }
    
    // ========== ПОДХОД 2: Итеративный ==========
    public List<List<Integer>> subsetsIterative(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        result.add(new ArrayList<>());  // Пустое подмножество
        
        for (int num : nums) {
            int size = result.size();
            for (int i = 0; i < size; i++) {
                List<Integer> newSubset = new ArrayList<>(result.get(i));
                newSubset.add(num);
                result.add(newSubset);
            }
        }
        
        return result;
    }
    
    // ========== ПОДХОД 3: Битовые маски ==========
    public List<List<Integer>> subsetsBitmask(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        int n = nums.length;
        
        for (int mask = 0; mask < (1 << n); mask++) {
            List<Integer> subset = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) != 0) {
                    subset.add(nums[i]);
                }
            }
            result.add(subset);
        }
        
        return result;
    }
}