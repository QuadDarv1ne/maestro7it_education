/**
 * https://leetcode.com/problems/container-with-most-water/description/
 */

class Solution {
    /**
     * Находит максимальную площадь контейнера для воды.
     *
     * @param height массив высот вертикальных линий
     * @return максимальная площадь контейнера
     *
     * Алгоритм:
     * - Используем два указателя: слева и справа.
     * - Площадь = (ширина) * min(высоты).
     * - Двигаем указатель с меньшей высотой.
     * - Сложность: O(n), память: O(1).
     */
    public int maxArea(int[] height) {
        int left = 0, right = height.length - 1;
        int maxArea = 0;
        while (left < right) {
            int area = (right - left) * Math.min(height[left], height[right]);
            maxArea = Math.max(maxArea, area);
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return maxArea;
    }
}

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