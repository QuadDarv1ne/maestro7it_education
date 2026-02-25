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
using System.Numerics;

public class Solution {
    /// <summary>
    /// Сортирует массив по количеству единичных битов,
    /// а затем по значению числа.
    /// </summary>
    /// <param name="arr">входной массив</param>
    /// <returns>отсортированный массив</returns>
    public int[] SortByBits(int[] arr) {
        // Используем Array.Sort с компаратором
        Array.Sort(arr, (a, b) => {
            int bitsA = BitOperations.PopCount((uint)a);
            int bitsB = BitOperations.PopCount((uint)b);
            if (bitsA == bitsB) return a.CompareTo(b);
            return bitsA.CompareTo(bitsB);
        });
        return arr;
    }
}