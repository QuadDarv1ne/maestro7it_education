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

class Solution {
    public long minimumCost(int[] nums, int k, int dist) {
        int n = nums.length;
        if (k == 1) return nums[0];
        
        TreeMap<Integer, Integer> selected = new TreeMap<>();
        TreeMap<Integer, Integer> candidates = new TreeMap<>();
        long selectedSum = 0;
        
        // Инициализация первого окна
        List<Integer> window = new ArrayList<>();
        for (int i = 1; i < Math.min(n, dist + 2); i++) {
            window.add(nums[i]);
        }
        Collections.sort(window);
        
        for (int i = 0; i < Math.min(window.size(), k - 1); i++) {
            int val = window.get(i);
            selected.put(val, selected.getOrDefault(val, 0) + 1);
            selectedSum += val;
        }
        for (int i = k - 1; i < window.size(); i++) {
            int val = window.get(i);
            candidates.put(val, candidates.getOrDefault(val, 0) + 1);
        }
        
        long minCost = nums[0] + selectedSum;
        
        // Скользим окном
        for (int right = dist + 2; right < n; right++) {
            int left = right - dist - 1;
            int outVal = nums[left];
            int inVal = nums[right];
            
            // Удаляем выходящий элемент
            if (selected.containsKey(outVal)) {
                selectedSum -= outVal;
                if (selected.get(outVal) == 1) {
                    selected.remove(outVal);
                } else {
                    selected.put(outVal, selected.get(outVal) - 1);
                }
                
                // Пополняем из candidates
                if (!candidates.isEmpty()) {
                    int minVal = candidates.firstKey();
                    selectedSum += minVal;
                    selected.put(minVal, selected.getOrDefault(minVal, 0) + 1);
                    if (candidates.get(minVal) == 1) {
                        candidates.remove(minVal);
                    } else {
                        candidates.put(minVal, candidates.get(minVal) - 1);
                    }
                }
            } else if (candidates.containsKey(outVal)) {
                if (candidates.get(outVal) == 1) {
                    candidates.remove(outVal);
                } else {
                    candidates.put(outVal, candidates.get(outVal) - 1);
                }
            }
            
            // Добавляем входящий элемент
            int selectedSize = selected.values().stream().mapToInt(Integer::intValue).sum();
            if (selectedSize < k - 1) {
                selected.put(inVal, selected.getOrDefault(inVal, 0) + 1);
                selectedSum += inVal;
            } else if (!selected.isEmpty() && inVal < selected.lastKey()) {
                int maxVal = selected.lastKey();
                selectedSum -= maxVal;
                if (selected.get(maxVal) == 1) {
                    selected.remove(maxVal);
                } else {
                    selected.put(maxVal, selected.get(maxVal) - 1);
                }
                candidates.put(maxVal, candidates.getOrDefault(maxVal, 0) + 1);
                
                selected.put(inVal, selected.getOrDefault(inVal, 0) + 1);
                selectedSum += inVal;
            } else {
                candidates.put(inVal, candidates.getOrDefault(inVal, 0) + 1);
            }
            
            minCost = Math.min(minCost, nums[0] + selectedSum);
        }
        
        return minCost;
    }
}