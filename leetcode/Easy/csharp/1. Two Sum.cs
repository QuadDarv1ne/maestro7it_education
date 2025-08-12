/**
 * https://leetcode.com/problems/two-sum/description/
 */

using System.Collections.Generic;

public class Solution {
    /**
     * Находит индексы двух чисел в массиве, сумма которых равна target.
     *
     * @param nums Массив целых чисел.
     * @param target Целевое значение суммы.
     * @return Массив из двух индексов чисел, сумма которых равна target.
     */
    public int[] TwoSum(int[] nums, int target) {
        Dictionary<int, int> seen = new Dictionary<int, int>();
        for (int i = 0; i < nums.Length; i++) {
            int complement = target - nums[i];
            if (seen.ContainsKey(complement)) {
                return new int[] { seen[complement], i };
            }
            seen[nums[i]] = i;
        }
        return new int[0];
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