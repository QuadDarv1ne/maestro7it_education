/**
 * https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/
 */

#include <vector>

/**
 * @brief Удаляет дубликаты из отсортированного массива.
 *
 * Алгоритм:
 *  - Метод двух указателей (медленный i и быстрый j).
 *  - Копируем новые уникальные элементы в начало массива.
 *
 * Время: O(n), Память: O(1)
 */
class Solution {
public:
    int removeDuplicates(std::vector<int>& nums) {
        if (nums.empty()) return 0;
        int i = 0;
        for (int j = 1; j < static_cast<int>(nums.size()); ++j) {
            if (nums[j] != nums[i]) {
                ++i;
                nums[i] = nums[j];
            }
        }
        return i + 1;
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