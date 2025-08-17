/**
 * https://leetcode.com/problems/validate-ip-address/description/
 */

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
 *
 * @param {string} queryIP
 * @return {string}
 */
var validIPAddress = function(queryIP) {
    if (queryIP.includes('.')) {
        let parts = queryIP.split('.');
        if (parts.length === 4) {
            for (let part of parts) {
                if (part.length === 0 || (part.length > 1 && part[0] === '0') || !/^\d+$/.test(part) || parseInt(part) > 255)
                    return "Neither";
            }
            return "IPv4";
        }
    } else if (queryIP.includes(':')) {
        let parts = queryIP.split(':');
        if (parts.length === 8) {
            for (let part of parts) {
                if (part.length === 0 || part.length > 4 || !/^[0-9a-fA-F]+$/.test(part))
                    return "Neither";
            }
            return "IPv6";
        }
    }
    return "Neither";
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