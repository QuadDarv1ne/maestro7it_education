/**
 * https://leetcode.com/problems/meeting-rooms/description/
 */

import java.util.Arrays;
import java.util.Comparator;

class Solution {
    /**
     * Проверяет, можно ли провести все встречи в одном помещении.
     * Алгоритм:
     * 1. Сортировка встреч по времени начала
     * 2. Проверка перекрытий между соседними встречами
     *
     * @param intervals Массив встреч [start, end]
     * @return true, если встречи не пересекаются, иначе false
     */
    public boolean canAttendMeetings(int[][] intervals) {
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

        for (int i = 1; i < intervals.length; i++) {
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