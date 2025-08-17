/**
 * https://leetcode.com/problems/intersection-of-two-arrays/description/
 */

import java.util.*;

class Solution {
    /**
     * Метод ищет пересечение двух массивов.
     * Каждый элемент результата уникален.
     *
     * @param nums1 первый массив чисел
     * @param nums2 второй массив чисел
     * @return массив уникальных элементов, встречающихся в обоих массивах
     */
    public int[] intersection(int[] nums1, int[] nums2) {
        Set<Integer> set1 = new HashSet<>();
        for (int num : nums1) set1.add(num);

        Set<Integer> result = new HashSet<>();
        for (int num : nums2) {
            if (set1.contains(num)) {
                result.add(num);
            }
        }

        int[] ans = new int[result.size()];
        int i = 0;
        for (int num : result) ans[i++] = num;
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