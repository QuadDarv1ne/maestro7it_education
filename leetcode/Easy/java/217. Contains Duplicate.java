/**
 * https://leetcode.com/problems/contains-duplicate/description/
 */

import java.util.HashSet;
import java.util.Set;

class Solution {
    /**
     * Проверяет массив на наличие дублирующихся элементов.
     * Используется HashSet для хранения уникальных значений.
     *
     * @param nums Входной массив целых чисел.
     * @return true, если найден дубликат; иначе false.
     */
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (!seen.add(num)) {
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