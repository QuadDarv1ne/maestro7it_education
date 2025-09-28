/**
 * https://leetcode.com/problems/largest-perimeter-triangle/description/?envType=daily-question&envId=2025-09-28
 */

import java.util.Arrays;

class Solution {
    public int largestPerimeter(int[] nums) {
        /*
        Находит максимальный периметр треугольника, который можно построить
        из трёх длин массива nums.

        Алгоритм:
        1. Сортируем массив.
        2. Перебираем массив с конца, беря тройки подряд.
        3. Проверяем условие треугольника (a + b > c).
        4. Если найдено — возвращаем периметр.
        5. Иначе возвращаем 0.
        */
        Arrays.sort(nums);
        int n = nums.length;
        for (int i = n - 1; i >= 2; i--) {
            int a = nums[i - 2], b = nums[i - 1], c = nums[i];
            if (a + b > c)
                return a + b + c;
        }
        return 0;
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/