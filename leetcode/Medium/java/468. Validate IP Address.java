/**
 * https://leetcode.com/problems/validate-ip-address/description/
 */

public class Solution {
    public String validIPAddress(String queryIP) {
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
        if (queryIP.chars().filter(ch -> ch == '.').count() == 3) { // IPv4 проверка
            String[] parts = queryIP.split("\\.", -1); // -1 чтобы сохранить пустые сегменты
            if (parts.length != 4) return "Neither";
            for (String part : parts) {
                if (part.length() == 0 || part.length() > 3) return "Neither";
                if (!part.matches("\\d+")) return "Neither";
                int num = Integer.parseInt(part);
                if (num < 0 || num > 255) return "Neither";
                if (part.length() > 1 && part.charAt(0) == '0') return "Neither"; // ведущие нули
            }
            return "IPv4";
        } else if (queryIP.chars().filter(ch -> ch == ':').count() == 7) { // IPv6 проверка
            String[] parts = queryIP.split(":", -1); // -1 чтобы сохранить пустые сегменты
            if (parts.length != 8) return "Neither";
            for (String part : parts) {
                if (part.length() == 0 || part.length() > 4) return "Neither";
                if (!part.matches("[0-9a-fA-F]+")) return "Neither";
            }
            return "IPv6";
        } else {
            return "Neither";
        }
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