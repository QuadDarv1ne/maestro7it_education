/**
 * https://leetcode.com/problems/intersection-of-two-arrays/description/
 */

#include <vector>
#include <unordered_set>
using namespace std;

class Solution {
public:
    /**
     * Метод ищет пересечение двух массивов.
     * Каждый элемент результата уникален.
     *
     * @param nums1 первый массив чисел
     * @param nums2 второй массив чисел
     * @return вектор уникальных элементов, встречающихся в обоих массивах
     */
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        unordered_set<int> set1(nums1.begin(), nums1.end());
        vector<int> result;
        for (int num : nums2) {
            if (set1.erase(num)) { // erase возвращает 1, если элемент был найден
                result.push_back(num);
            }
        }
        return result;
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