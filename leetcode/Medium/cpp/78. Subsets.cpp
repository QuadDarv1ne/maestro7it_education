/* ========================== C++ ========================== */

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

#include <vector>
using namespace std;

class Solution {
public:
    // ========== ПОДХОД 1: Backtracking ==========
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> path;
        backtrack(nums, 0, path, result);
        return result;
    }
    
private:
    void backtrack(vector<int>& nums, int index, 
                   vector<int>& path, vector<vector<int>>& result) {
        // Каждый путь - валидное подмножество
        result.push_back(path);
        
        // Пробуем добавить оставшиеся элементы
        for (int i = index; i < nums.size(); i++) {
            path.push_back(nums[i]);
            backtrack(nums, i + 1, path, result);
            path.pop_back();
        }
    }
    
public:
    // ========== ПОДХОД 2: Итеративный ==========
    vector<vector<int>> subsetsIterative(vector<int>& nums) {
        vector<vector<int>> result = {{}};  // Пустое подмножество
        
        for (int num : nums) {
            int size = result.size();
            for (int i = 0; i < size; i++) {
                vector<int> newSubset = result[i];
                newSubset.push_back(num);
                result.push_back(newSubset);
            }
        }
        
        return result;
    }
    
    // ========== ПОДХОД 3: Битовые маски ==========
    vector<vector<int>> subsetsBitmask(vector<int>& nums) {
        vector<vector<int>> result;
        int n = nums.size();
        
        for (int mask = 0; mask < (1 << n); mask++) {
            vector<int> subset;
            for (int i = 0; i < n; i++) {
                if (mask & (1 << i)) {
                    subset.push_back(nums[i]);
                }
            }
            result.push_back(subset);
        }
        
        return result;
    }
};