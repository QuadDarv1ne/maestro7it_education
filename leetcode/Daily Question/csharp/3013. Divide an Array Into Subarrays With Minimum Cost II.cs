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

public class Solution {
    public long MinimumCost(int[] nums, int k, int dist) {
        int n = nums.Length;
        if (k == 1) return nums[0];
        
        SortedSet<(int value, int index)> selected = new SortedSet<(int, int)>();
        SortedSet<(int value, int index)> candidates = new SortedSet<(int, int)>();
        long selectedSum = 0;
        int uniqueIndex = 0;
        
        // Инициализация первого окна
        List<(int value, int index)> window = new List<(int, int)>();
        for (int i = 1; i < Math.Min(n, dist + 2); i++) {
            window.Add((nums[i], uniqueIndex++));
        }
        window.Sort();
        
        for (int i = 0; i < Math.Min(window.Count, k - 1); i++) {
            selected.Add(window[i]);
            selectedSum += window[i].value;
        }
        for (int i = k - 1; i < window.Count; i++) {
            candidates.Add(window[i]);
        }
        
        long minCost = nums[0] + selectedSum;
        
        // Скользим окном
        for (int right = dist + 2; right < n; right++) {
            int left = right - dist - 1;
            int outVal = nums[left];
            int inVal = nums[right];
            
            // Удаляем выходящий элемент
            var toRemove = selected.FirstOrDefault(x => x.value == outVal);
            if (toRemove != default) {
                selected.Remove(toRemove);
                selectedSum -= outVal;
                
                // Пополняем из candidates
                if (candidates.Count > 0) {
                    var minCandidate = candidates.Min;
                    candidates.Remove(minCandidate);
                    selected.Add(minCandidate);
                    selectedSum += minCandidate.value;
                }
            } else {
                toRemove = candidates.FirstOrDefault(x => x.value == outVal);
                if (toRemove != default) {
                    candidates.Remove(toRemove);
                }
            }
            
            // Добавляем входящий элемент
            var newElement = (inVal, uniqueIndex++);
            if (selected.Count < k - 1) {
                selected.Add(newElement);
                selectedSum += inVal;
            } else if (inVal < selected.Max.value) {
                var maxSelected = selected.Max;
                selected.Remove(maxSelected);
                selectedSum -= maxSelected.value;
                candidates.Add(maxSelected);
                
                selected.Add(newElement);
                selectedSum += inVal;
            } else {
                candidates.Add(newElement);
            }
            
            minCost = Math.Min(minCost, nums[0] + selectedSum);
        }
        
        return minCost;
    }
}