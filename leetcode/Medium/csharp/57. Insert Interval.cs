/**
 * https://leetcode.com/problems/insert-interval/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Insert Interval" на C#
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
    public int[][] Insert(int[][] intervals, int[] newInterval) {
        var result = new List<int[]>();
        int i = 0;
        int n = intervals.Length;
        
        // Добавляем интервалы, которые заканчиваются до начала нового
        while (i < n && intervals[i][1] < newInterval[0]) {
            result.Add(intervals[i]);
            i++;
        }
        
        // Объединяем пересекающиеся интервалы
        while (i < n && intervals[i][0] <= newInterval[1]) {
            newInterval[0] = Math.Min(newInterval[0], intervals[i][0]);
            newInterval[1] = Math.Max(newInterval[1], intervals[i][1]);
            i++;
        }
        result.Add(newInterval);
        
        // Добавляем оставшиеся интервалы
        while (i < n) {
            result.Add(intervals[i]);
            i++;
        }
        
        return result.ToArray();
    }
}