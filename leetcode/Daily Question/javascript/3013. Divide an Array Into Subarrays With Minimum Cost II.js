/**
 * Решение задачи LeetCode № 3013: "Divide an Array Into Subarrays With Minimum Cost II"
 * https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
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

/**
 * @param {number[]} nums
 * @param {number} k
 * @param {number} dist
 * @return {number}
 */
var minimumCost = function(nums, k, dist) {
    const n = nums.length;
    if (k === 1) return nums[0];
    
    // Используем массивы для имитации multiset
    let selected = [];    // k-1 наименьших элементов (отсортированы)
    let candidates = [];  // остальные элементы (отсортированы)
    let selectedSum = 0;
    
    // Инициализация первого окна
    const window = [];
    for (let i = 1; i < Math.min(n, dist + 2); i++) {
        window.push(nums[i]);
    }
    window.sort((a, b) => a - b);
    
    selected = window.slice(0, Math.min(window.length, k - 1));
    selectedSum = selected.reduce((sum, val) => sum + val, 0);
    candidates = window.slice(k - 1);
    
    let minCost = nums[0] + selectedSum;
    
    // Функция для вставки элемента в отсортированный массив
    const insertSorted = (arr, val) => {
        let left = 0, right = arr.length;
        while (left < right) {
            const mid = Math.floor((left + right) / 2);
            if (arr[mid] < val) left = mid + 1;
            else right = mid;
        }
        arr.splice(left, 0, val);
    };
    
    // Функция для удаления первого вхождения элемента
    const removeFirst = (arr, val) => {
        const idx = arr.indexOf(val);
        if (idx !== -1) {
            arr.splice(idx, 1);
            return true;
        }
        return false;
    };
    
    // Скользим окном
    for (let right = dist + 2; right < n; right++) {
        const left = right - dist - 1;
        const outVal = nums[left];
        const inVal = nums[right];
        
        // Удаляем выходящий элемент
        if (removeFirst(selected, outVal)) {
            selectedSum -= outVal;
            
            // Пополняем из candidates
            if (candidates.length > 0) {
                const val = candidates.shift();
                insertSorted(selected, val);
                selectedSum += val;
            }
        } else {
            removeFirst(candidates, outVal);
        }
        
        // Добавляем входящий элемент
        if (selected.length < k - 1) {
            insertSorted(selected, inVal);
            selectedSum += inVal;
        } else if (inVal < selected[selected.length - 1]) {
            const maxVal = selected.pop();
            selectedSum -= maxVal;
            insertSorted(candidates, maxVal);
            
            insertSorted(selected, inVal);
            selectedSum += inVal;
        } else {
            insertSorted(candidates, inVal);
        }
        
        minCost = Math.min(minCost, nums[0] + selectedSum);
    }
    
    return minCost;
};