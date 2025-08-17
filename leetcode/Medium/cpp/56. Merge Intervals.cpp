/**
 * https://leetcode.com/problems/merge-intervals/description/
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * Объединяет все перекрывающиеся интервалы в массиве intervals.
     *
     * @param intervals Вектор интервалов, каждый представлен парой [start, end].
     * @return Вектор объединённых интервалов.
     */
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        if (intervals.empty()) return {};

        sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) {
            return a[0] < b[0];
        });

        vector<vector<int>> merged;
        merged.push_back(intervals[0]);

        for (auto& current : intervals) {
            if (current[0] <= merged.back()[1]) {
                merged.back()[1] = max(merged.back()[1], current[1]);
            } else {
                merged.push_back(current);
            }
        }

        return merged;
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