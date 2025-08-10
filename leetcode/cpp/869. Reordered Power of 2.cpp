/**
 * https://leetcode.com/problems/reordered-power-of-2/description/
 */

#include <algorithm>
#include <string>

class Solution {
public:
    bool reorderedPowerOf2(int N) {
        std::string nStr = std::to_string(N);
        std::sort(nStr.begin(), nStr.end());
        int nLen = nStr.length();
        
        for (int i = 0; ; i++) {
            long num = 1L << i;
            std::string numStr = std::to_string(num);
            if (numStr.length() > nLen) {
                break;
            } else if (numStr.length() < nLen) {
                continue;
            }
            std::sort(numStr.begin(), numStr.end());
            if (numStr == nStr) {
                return true;
            }
        }
        return false;
    }
};

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
