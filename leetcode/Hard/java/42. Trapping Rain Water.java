/**
 * https://leetcode.com/problems/trapping-rain-water/description/?envType=study-plan-v2&envId=top-interview-150
 */

class Solution {
    /**
     * Вычисляет объем воды, который можно собрать после дождя между столбцами.
     *
     * Алгоритм:
     * 1. Два указателя: left и right.
     * 2. leftMax хранит макс. высоту слева, rightMax — справа.
     * 3. Если height[left] < height[right]:
     *    - Если height[left] >= leftMax, обновляем leftMax.
     *    - Иначе добавляем (leftMax - height[left]) в воду.
     * 4. Иначе аналогично обрабатываем правый указатель.
     *
     * @param height массив высот столбцов.
     * @return объем накопленной воды.
     *
     * Сложность:
     * Время: O(n)
     * Память: O(1)
     */
    public int trap(int[] height) {
        if (height == null || height.length == 0) return 0;

        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0, water = 0;

        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax)
                    leftMax = height[left];
                else
                    water += leftMax - height[left];
                left++;
            } else {
                if (height[right] >= rightMax)
                    rightMax = height[right];
                else
                    water += rightMax - height[right];
                right--;
            }
        }
        return water;
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