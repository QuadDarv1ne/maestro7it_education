/**
 * https://leetcode.com/problems/merge-intervals/description/
 */

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Объединяет все перекрывающиеся интервалы в массиве intervals.
    /// </summary>
    /// <param name="intervals">Массив интервалов, каждый представлен парой [start, end].</param>
    /// <returns>Массив объединённых интервалов.</returns>
    public int[][] Merge(int[][] intervals) {
        if (intervals.Length == 0) return new int[0][];

        Array.Sort(intervals, (a, b) => a[0].CompareTo(b[0]));
        var merged = new List<int[]>();
        merged.Add(new int[] { intervals[0][0], intervals[0][1] });

        foreach (var current in intervals) {
            var last = merged[merged.Count - 1];
            if (current[0] <= last[1]) {
                last[1] = Math.Max(last[1], current[1]);
            } else {
                merged.Add(new int[] { current[0], current[1] });
            }
        }

        // Преобразуем List<int[]> в int[][]
        return merged.ToArray();
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/