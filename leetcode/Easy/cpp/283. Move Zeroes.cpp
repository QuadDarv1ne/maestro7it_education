/**
 * https://leetcode.com/problems/move-zeroes/description/
 */

#include <vector>
#include <algorithm>

/**
 * @brief Перемещает все нули в конец массива, сохраняя порядок ненулевых элементов.
 *
 * Алгоритм:
 *  - Используется метод двух указателей: i (позиция для следующего ненулевого элемента) 
 *    и j (текущий индекс).
 *  - Когда nums[j] != 0, меняем nums[i] и nums[j], увеличиваем i.
 *
 * Время работы: O(n)
 * Память: O(1)
 */
class Solution {
public:
    void moveZeroes(std::vector<int>& nums) {
        int i = 0;
        for (int j = 0; j < nums.size(); ++j) {
            if (nums[j] != 0) {
                std::swap(nums[i], nums[j]);
                ++i;
            }
        }
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