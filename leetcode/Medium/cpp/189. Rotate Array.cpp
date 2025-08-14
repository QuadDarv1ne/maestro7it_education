/**
 * https://leetcode.com/problems/rotate-array/description/
 */

#include <vector>
#include <algorithm>

class Solution {
public:
    /**
     * @brief Поворот массива вправо на k позиций
     * 
     * Функция принимает массив nums и целое число k. Она изменяет массив in-place,
     * поворачивая его элементы вправо на k шагов.
     * 
     * @param nums - ссылка на вектор целых чисел
     * @param k - число шагов для поворота массива
     */
    void rotate(std::vector<int>& nums, int k) {
        int n = nums.size();
        k %= n; // на случай, если k > n
        std::reverse(nums.begin(), nums.end());
        std::reverse(nums.begin(), nums.begin() + k);
        std::reverse(nums.begin() + k, nums.end());
    }
};

// Solution().rotate(nums, k);

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