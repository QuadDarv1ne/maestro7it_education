/**
 * https://leetcode.com/problems/reverse-integer/description/
 */

/// <summary>
/// Переворачивает цифры числа x и возвращает результат.
/// Если перевёрнутое число выходит за пределы 32-битного диапазона, возвращает 0.
/// </summary>
public class Solution {
    public int Reverse(int x) {
        long reversed = 0; // используем long для предотвращения переполнения
        while (x != 0) {
            int digit = x % 10;
            reversed = reversed * 10 + digit;
            if (reversed > int.MaxValue || reversed < int.MinValue)
                return 0;
            x /= 10;
        }
        return (int)reversed;
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