/**
 * https://leetcode.com/problems/reordered-power-of-2/description/
 */

import java.util.Arrays;

class Solution {
    public boolean reorderedPowerOf2(int N) {
        String nStr = Integer.toString(N);
        char[] nArr = nStr.toCharArray();
        Arrays.sort(nArr);
        String sortedN = new String(nArr);
        int nLen = nStr.length();
        
        for (int i = 0; ; i++) {
            long num = (1L << i);
            String numStr = Long.toString(num);
            if (numStr.length() > nLen) {
                break;
            } else if (numStr.length() < nLen) {
                continue;
            }
            char[] numArr = numStr.toCharArray();
            Arrays.sort(numArr);
            String sortedPower = new String(numArr);
            if (sortedPower.equals(sortedN)) {
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
