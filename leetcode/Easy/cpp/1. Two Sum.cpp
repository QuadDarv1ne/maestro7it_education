/**
 * https://leetcode.com/problems/two-sum/description/
 */

#include <vector>
#include <unordered_map>

using namespace std;

class Solution {
public:
    /**
     * Находит индексы двух чисел в массиве, сумма которых равна target.
     *
     * @param nums Вектор целых чисел.
     * @param target Целевое значение суммы.
     * @return Вектор из двух индексов чисел, сумма которых равна target.
     */
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen;  // Хэш-таблица для хранения значений и их индексов
        for (int i = 0; i < nums.size(); ++i) {
            int complement = target - nums[i];
            if (seen.find(complement) != seen.end()) {
                return {seen[complement], i};
            }
            seen[nums[i]] = i;
        }
        return {};
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