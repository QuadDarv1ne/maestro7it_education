/**
 * https://leetcode.com/problems/maximum-69-number/description/?envType=daily-question&envId=2025-08-16
 */

class Solution {
public:
    /**
     * Меняем первую '6' на '9' слева направо.
     */
    int maximum69Number (int num) {
        string s = to_string(num);
        for (char &c : s) {
            if (c == '6') {
                c = '9';
                break;
            }
        }
        return stoi(s);
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