/**
 * https://leetcode.com/problems/reverse-integer/description/
 */

#include <climits>

/**
 * @brief Переворачивает цифры числа x и возвращает результат.
 * Если перевёрнутое число выходит за пределы 32-битного диапазона, возвращает 0.
 */
class Solution {
public:
    int reverse(int x) {
        long reversed = 0;  // используем long, чтобы избежать переполнения во время вычислений
        while (x != 0) {
            int digit = x % 10;
            reversed = reversed * 10 + digit;
            if (reversed > INT_MAX || reversed < INT_MIN)
                return 0;
            x /= 10;
        }
        return static_cast<int>(reversed);
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