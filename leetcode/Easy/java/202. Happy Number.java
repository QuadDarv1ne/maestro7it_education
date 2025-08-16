/**
 * https://leetcode.com/problems/happy-number/description/
 */

import java.util.*;

class Solution {
    public boolean isHappy(int n) {
        /*
         Используем HashSet для отслеживания уже встреченных чисел.
        */
        Set<Integer> seen = new HashSet<>();
        while (n != 1 && !seen.contains(n)) {
            seen.add(n);
            int next = 0;
            while (n > 0) {
                int d = n % 10;
                next += d * d;
                n /= 10;
            }
            n = next;
        }
        return n == 1;
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