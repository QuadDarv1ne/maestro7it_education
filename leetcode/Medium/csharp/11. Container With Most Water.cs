/**
 * https://leetcode.com/problems/container-with-most-water/description/
 */

public class Solution {
    /// <summary>
    /// Находит максимальную площадь контейнера для воды.
    /// 
    /// height[i] — высота линии. 
    /// Нужно выбрать две линии, чтобы площадь была максимальной.
    /// 
    /// Алгоритм:
    /// - Два указателя (слева и справа).
    /// - Площадь = (ширина) * min(высоты).
    /// - Двигаем меньший по высоте указатель.
    /// - Сложность: O(n), память: O(1).
    /// </summary>
    public int MaxArea(int[] height) {
        int left = 0, right = height.Length - 1;
        int maxArea = 0;
        while (left < right) {
            int area = (right - left) * Math.Min(height[left], height[right]);
            maxArea = Math.Max(maxArea, area);
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