/**
 * https://leetcode.com/problems/intersection-of-two-arrays/description/
 */

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Метод ищет пересечение двух массивов.
    /// Каждый элемент результата уникален.
    /// </summary>
    /// <param name="nums1">первый массив чисел</param>
    /// <param name="nums2">второй массив чисел</param>
    /// <returns>массив уникальных элементов, встречающихся в обоих массивах</returns>
    public int[] Intersection(int[] nums1, int[] nums2) {
        HashSet<int> set1 = new HashSet<int>(nums1);
        HashSet<int> result = new HashSet<int>();

        foreach (int num in nums2) {
            if (set1.Contains(num)) {
                result.Add(num);
            }
        }

        int[] ans = new int[result.Count];
        result.CopyTo(ans);
        return ans;
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