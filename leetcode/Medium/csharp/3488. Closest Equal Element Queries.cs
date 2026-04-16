/**
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

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Находит минимальное кольцевое расстояние до ДРУГОГО равного элемента.
    /// </summary>
    public int[] SolveQueries(int[] nums, int[] queries) {
        int n = nums.Length;
        var indexMap = new Dictionary<int, List<int>>();
        
        for (int i = 0; i < n; i++) {
            if (!indexMap.ContainsKey(nums[i])) {
                indexMap[nums[i]] = new List<int>();
            }
            indexMap[nums[i]].Add(i);
        }
        
        int[] answer = new int[queries.Length];
        
        for (int i = 0; i < queries.Length; i++) {
            int q = queries[i];
            int val = nums[q];
            var pos = indexMap[val];
            int m = pos.Count;
            
            if (m == 1) {
                answer[i] = -1;
                continue;
            }
            
            // Бинарный поиск
            int idx = pos.BinarySearch(q);
            // В C# BinarySearch возвращает индекс, т.к. q точно есть в pos
            
            // Соседи
            int leftIdx = (idx - 1 + m) % m;
            int rightIdx = (idx + 1) % m;
            
            int leftPos = pos[leftIdx];
            int rightPos = pos[rightIdx];
            
            // Расстояния
            int dLeft = Math.Abs(q - leftPos);
            int distLeft = Math.Min(dLeft, n - dLeft);
            
            int dRight = Math.Abs(q - rightPos);
            int distRight = Math.Min(dRight, n - dRight);
            
            answer[i] = Math.Min(distLeft, distRight);
        }
        
        return answer;
    }
}