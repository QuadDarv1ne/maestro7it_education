/* ========================== JAVASCRIPT ========================== */

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

// ========== ПОДХОД 1: Backtracking ==========
/**
 * @param {number[]} nums
 * @return {number[][]}
 */
var subsets = function(nums) {
    const result = [];
    
    const backtrack = (index, path) => {
        // Каждый путь - валидное подмножество
        result.push([...path]);
        
        // Пробуем добавить оставшиеся элементы
        for (let i = index; i < nums.length; i++) {
            path.push(nums[i]);
            backtrack(i + 1, path);
            path.pop();
        }
    };
    
    backtrack(0, []);
    return result;
};

// ========== ПОДХОД 2: Итеративный ==========
var subsetsIterative = function(nums) {
    let result = [[]];  // Начинаем с пустого подмножества
    
    for (const num of nums) {
        const newSubsets = [];
        for (const subset of result) {
            newSubsets.push([...subset, num]);
        }
        result = result.concat(newSubsets);
    }
    
    return result;
};

// ========== ПОДХОД 3: Битовые маски ==========
var subsetsBitmask = function(nums) {
    const result = [];
    const n = nums.length;
    
    for (let mask = 0; mask < (1 << n); mask++) {
        const subset = [];
        for (let i = 0; i < n; i++) {
            if (mask & (1 << i)) {
                subset.push(nums[i]);
            }
        }
        result.push(subset);
    }
    
    return result;
};