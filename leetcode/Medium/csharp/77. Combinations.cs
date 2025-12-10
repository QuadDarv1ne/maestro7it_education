/* ========================== C# ========================== */

/*
 * LeetCode 77: Combinations
 * https://leetcode.com/problems/combinations/
 * 
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
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
    /**
     * Генерирует все комбинации из k чисел в диапазоне [1, n].
     * 
     * Time Complexity: O(C(n,k) * k)
     * Space Complexity: O(k)
     */
    public IList<IList<int>> Combine(int n, int k) {
        IList<IList<int>> result = new List<IList<int>>();
        Backtrack(n, k, 1, new List<int>(), result);
        return result;
    }
    
    private void Backtrack(int n, int k, int start, 
                          List<int> path, IList<IList<int>> result) {
        // Базовый случай: комбинация готова
        if (path.Count == k) {
            result.Add(new List<int>(path));
            return;
        }
        
        // Оптимизация: i <= n - (k - path.Count) + 1
        for (int i = start; i <= n - (k - path.Count) + 1; i++) {
            // Выбираем число i
            path.Add(i);
            
            // Рекурсивно строим остальную часть
            Backtrack(n, k, i + 1, path, result);
            
            // Откатываем выбор (backtracking)
            path.RemoveAt(path.Count - 1);
        }
    }
}