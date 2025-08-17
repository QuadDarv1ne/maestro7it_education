/**
 * https://leetcode.com/problems/meeting-rooms/description/
 */

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Проверяет, можно ли провести все встречи в одном помещении.
    /// Алгоритм:
    /// 1. Сортировка встреч по времени начала
    /// 2. Проверка перекрытий между соседними встречами
    /// </summary>
    /// <param name="intervals">Список встреч [start, end]</param>
    /// <returns>true, если встречи не пересекаются, иначе false</returns>
    public bool CanAttendMeetings(int[][] intervals) {
        Array.Sort(intervals, (a, b) => a[0].CompareTo(b[0]));

        for (int i = 1; i < intervals.Length; i++) {
            if (intervals[i][0] < intervals[i-1][1])
                return false;
        }
        return true;
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