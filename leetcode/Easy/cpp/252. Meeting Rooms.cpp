/**
 * https://leetcode.com/problems/meeting-rooms/description/
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * Проверяет, можно ли провести все встречи в одном помещении.
     *
     * Алгоритм:
     * 1. Сортируем встречи по времени начала.
     * 2. Проверяем перекрытия между соседними встречами.
     *
     * @param intervals Вектор встреч [start, end]
     * @return true, если встречи не пересекаются, иначе false
     */
    bool canAttendMeetings(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b){
            return a[0] < b[0];
        });

        for (int i = 1; i < intervals.size(); ++i) {
            if (intervals[i][0] < intervals[i-1][1])
                return false;
        }
        return true;
    }
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