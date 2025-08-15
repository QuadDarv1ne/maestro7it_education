/**
 * https://leetcode.com/problems/contains-duplicate/description/
 */

using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Проверяет, содержит ли массив повторяющиеся числа.
    /// Используется HashSet для быстрой проверки существования элемента.
    /// </summary>
    /// <param name="nums">Массив целых чисел.</param>
    /// <returns>True, если есть дубликат; иначе False.</returns>
    public bool ContainsDuplicate(int[] nums) {
        HashSet<int> seen = new HashSet<int>();
        foreach (int num in nums) {
            if (!seen.Add(num)) {
                return true;
            }
        }
        return false;
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