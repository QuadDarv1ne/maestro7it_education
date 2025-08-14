/**
 * https://leetcode.com/problems/roman-to-integer/description/
 */

import java.util.HashMap;
import java.util.Map;

/**
 * Преобразует римское число s в целое число.
 */
class Solution {
    public int romanToInt(String s) {
        Map<Character, Integer> romanMap = new HashMap<>();
        romanMap.put('I', 1); romanMap.put('V', 5);
        romanMap.put('X', 10); romanMap.put('L', 50);
        romanMap.put('C', 100); romanMap.put('D', 500);
        romanMap.put('M', 1000);

        int total = 0;
        for (int i = 0; i < s.length() - 1; i++) {
            if (romanMap.get(s.charAt(i)) < romanMap.get(s.charAt(i + 1))) {
                total -= romanMap.get(s.charAt(i));
            } else {
                total += romanMap.get(s.charAt(i));
            }
        }
        total += romanMap.get(s.charAt(s.length() - 1));
        return total;
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