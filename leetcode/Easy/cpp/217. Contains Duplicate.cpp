/**
 * https://leetcode.com/problems/contains-duplicate/description/
 */

#include <vector>
#include <unordered_set>
using namespace std;

class Solution {
public:
    /**
     * Проверяет наличие дублирующихся элементов в массиве.
     * Использует unordered_set для быстрого поиска.
     *
     * @param nums – вектор целых чисел.
     * @return true, если обнаружен дубликат; иначе false.
     */
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> seen;
        for (int num : nums) {
            auto [it, inserted] = seen.insert(num);
            if (!inserted) return true;
        }
        return false;
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