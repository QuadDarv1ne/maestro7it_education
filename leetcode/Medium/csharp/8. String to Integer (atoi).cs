/**
 * https://leetcode.com/problems/string-to-integer-atoi/description/
 */

/// <summary>
/// Преобразует строку s в 32-битное знаковое целое число.
/// Обрабатывает пробелы, знак числа, недопустимые символы
/// и переполнение.
/// </summary>
public class Solution {
    public int MyAtoi(string s) {
        int i = 0, n = s.Length;
        while (i < n && s[i] == ' ') i++;

        if (i == n) return 0;

        int sign = 1;
        if (s[i] == '-') { sign = -1; i++; }
        else if (s[i] == '+') { i++; }

        long result = 0;
        while (i < n && char.IsDigit(s[i])) {
            int digit = s[i] - '0';
            result = result * 10 + digit;
            if (result * sign > int.MaxValue) return int.MaxValue;
            if (result * sign < int.MinValue) return int.MinValue;
            i++;
        }

        return (int)(sign * result);
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