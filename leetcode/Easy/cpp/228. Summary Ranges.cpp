/**
 * https://leetcode.com/problems/summary-ranges/description/?envType=study-plan-v2&envId=top-interview-150
 */

#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    /**
     * Функция принимает отсортированный вектор уникальных целых чисел и возвращает вектор строк,
     * представляющих минимальные диапазоны последовательных чисел.
     * 
     * @param nums - отсортированный вектор уникальных чисел
     * @return вектор строк с диапазонами в формате "start->end" или "start" если диапазон из одного числа
     */
    vector<string> summaryRanges(const vector<int>& nums) {
        vector<string> ranges;
        int n = nums.size();
        int i = 0;

        while (i < n) {
            int start = nums[i];
            while (i + 1 < n && nums[i + 1] == nums[i] + 1) {
                i++;
            }
            if (start == nums[i]) {
                ranges.push_back(to_string(start));
            } else {
                ranges.push_back(to_string(start) + "->" + to_string(nums[i]));
            }
            i++;
        }

        return ranges;
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