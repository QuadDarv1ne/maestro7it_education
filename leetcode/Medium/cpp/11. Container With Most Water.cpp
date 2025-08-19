/**
 * https://leetcode.com/problems/container-with-most-water/description/
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * Находит максимальную площадь контейнера для воды.
     *
     * height[i] — высота вертикальных линий. 
     * Нужно выбрать две линии, чтобы площадь контейнера была максимальной.
     *
     * Алгоритм:
     * - Два указателя: слева и справа.
     * - Считаем площадь = ширина * min(высоты).
     * - Двигаем внутрь тот указатель, у которого линия ниже.
     * - Сложность: O(n), память O(1).
     *
     * @param height вектор высот
     * @return максимальная площадь контейнера
     */
    int maxArea(vector<int>& height) {
        int left = 0, right = height.size() - 1, max_area = 0;
        while (left < right) {
            int area = (right - left) * min(height[left], height[right]);
            max_area = max(max_area, area);
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return max_area;
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