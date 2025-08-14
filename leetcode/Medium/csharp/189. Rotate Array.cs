/**
 * https://leetcode.com/problems/rotate-array/description/
 */

using System;

public class Solution {
    /// <summary>
    /// Поворот массива вправо на k позиций
    /// </summary>
    /// <param name="nums">Массив целых чисел</param>
    /// <param name="k">Число шагов для поворота массива</param>
    public void Rotate(int[] nums, int k) {
        int n = nums.Length;
        k %= n;

        void Reverse(int start, int end) {
            while (start < end) {
                int temp = nums[start];
                nums[start] = nums[end];
                nums[end] = temp;
                start++;
                end--;
            }
        }

        Reverse(0, n - 1);
        Reverse(0, k - 1);
        Reverse(k, n - 1);
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