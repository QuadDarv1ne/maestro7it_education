/**
 * https://leetcode.com/problems/happy-number/description/
 */

#include <vector>
#include <string>
#include <unordered_map>
#include <array>
using namespace std;

class Solution {
public:
    bool isHappy(int n) {
        /*
         Задача: определить, является ли число "счастливым".
         Используем правило: суммируем квадраты цифр до тех пор,
         пока не попадем в 1 (счастливое) или в цикл.
        */
        unordered_set<int> seen;
        while (n != 1 && !seen.count(n)) {
            seen.insert(n);
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