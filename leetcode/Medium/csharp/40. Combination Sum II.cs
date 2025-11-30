/**
 * https://leetcode.com/problems/combination-sum-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Combination Sum II" на C#
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
    public IList<IList<int>> CombinationSum2(int[] candidates, int target) {
        var result = new List<IList<int>>();
        Array.Sort(candidates);
        Backtrack(candidates, target, 0, new List<int>(), result);
        return result;
    }
    
    private void Backtrack(int[] candidates, int remaining, int start, 
                          List<int> current, List<IList<int>> result) {
        if (remaining == 0) {
            result.Add(new List<int>(current));
            return;
        }
        
        for (int i = start; i < candidates.Length; i++) {
            // Пропускаем дубликаты
            if (i > start && candidates[i] == candidates[i-1]) {
                continue;
            }
            
            if (candidates[i] > remaining) {
                break;
            }
            
            current.Add(candidates[i]);
            Backtrack(candidates, remaining - candidates[i], i + 1, current, result);
            current.RemoveAt(current.Count - 1);
        }
    }
}