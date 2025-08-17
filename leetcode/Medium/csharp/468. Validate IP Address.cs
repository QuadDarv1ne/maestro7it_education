/**
 * https://leetcode.com/problems/validate-ip-address/description/
 */

using System;

public class Solution {
    public string ValidIPAddress(string queryIP) {
        /**
         * Проверяет, является ли строка queryIP допустимым IPv4 или IPv6 адресом.
         *
         * Алгоритм:
         * 1. Если строка содержит точку ('.'), проверяем как IPv4.
         * 2. Если строка содержит двоеточие (':'), проверяем как IPv6.
         * 3. Если строка не содержит ни того, ни другого, возвращаем 'Neither'.
         *
         * Время: O(n), где n — длина строки queryIP.
         * Память: O(1).
         */
        if (queryIP.Contains('.')) {
            var parts = queryIP.Split('.');
            if (parts.Length == 4) {
                foreach (var part in parts) {
                    if (part.Length == 0 || (part.Length > 1 && part[0] == '0') || !int.TryParse(part, out int num) || num < 0 || num > 255)
                        return "Neither";
                }
                return "IPv4";
            }
        } else if (queryIP.Contains(':')) {
            var parts = queryIP.Split(':');
            if (parts.Length == 8) {
                foreach (var part in parts) {
                    if (part.Length == 0 || part.Length > 4 || !IsHexadecimal(part))
                        return "Neither";
                }
                return "IPv6";
            }
        }
        return "Neither";
    }

    private bool IsHexadecimal(string s) {
        foreach (var c in s) {
            if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F')))
                return false;
        }
        return true;
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