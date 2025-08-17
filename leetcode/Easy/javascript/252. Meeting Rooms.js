/**
 * https://leetcode.com/problems/meeting-rooms/description/
 */

/**
 * Проверяет, можно ли провести все встречи в одном помещении.
 * Алгоритм:
 * 1. Сортировка встреч по времени начала
 * 2. Проверка перекрытий между соседними встречами
 *
 * @param {number[][]} intervals Массив встреч [start, end]
 * @return {boolean} true, если встречи не пересекаются, иначе false
 */
var canAttendMeetings = function(intervals) {
    intervals.sort((a, b) => a[0] - b[0]);
    
    for (let i = 1; i < intervals.length; i++) {
        if (intervals[i][0] < intervals[i-1][1])
            return false;
    }
    return true;
};

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