/**
 * https://leetcode.com/problems/trapping-rain-water/description/?envType=study-plan-v2&envId=top-interview-150
 */

#include <vector>
using namespace std;

class Solution {
public:
    /**
     * @brief Вычисляет объем воды, который можно собрать после дождя между столбцами.
     * 
     * Алгоритм:
     * - Используется метод двух указателей: один идет слева (left), другой справа (right).
     * - leftMax хранит максимальную высоту слева, rightMax — справа.
     * - Если текущая высота слева меньше, чем справа, обрабатываем левый указатель:
     *   - Если высота >= leftMax, обновляем leftMax.
     *   - Иначе добавляем (leftMax - height[left]) в объем воды.
     * - Аналогично обрабатывается правый указатель.
     * 
     * @param height Вектор высот столбцов.
     * @return int — общий объем накопленной воды.
     * 
     * Сложность:
     * - Время: O(n), где n — количество столбцов.
     * - Память: O(1) дополнительная.
     */
    int trap(vector<int>& height) {
        if (height.empty()) return 0;

        int left = 0, right = height.size() - 1;
        int leftMax = 0, rightMax = 0, water = 0;

        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax)
                    leftMax = height[left];
                else
                    water += leftMax - height[left];
                ++left;
            } else {
                if (height[right] >= rightMax)
                    rightMax = height[right];
                else
                    water += rightMax - height[right];
                --right;
            }
        }
        return water;
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