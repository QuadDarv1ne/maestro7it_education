/**
 * https://leetcode.com/problems/binary-watch/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "401. Binary Watch"
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

/**
 * @param {number} turnedOn
 * @return {string[]}
 */
var readBinaryWatch = function(turnedOn) {
    const result = [];
    for (let hour = 0; hour < 12; hour++) {
        for (let minute = 0; minute < 60; minute++) {
            // Подсчёт битов: переводим в двоичную строку и считаем единицы
            const bitsHour = hour.toString(2).split('1').length - 1;
            const bitsMinute = minute.toString(2).split('1').length - 1;
            if (bitsHour + bitsMinute === turnedOn) {
                result.push(`${hour}:${minute.toString().padStart(2, '0')}`);
            }
        }
    }
    return result;
};