/**
 * https://leetcode.com/problems/reverse-string/description/
 */

/**
 * Переворачивает массив символов на месте.
 * Изменяет входной массив так, что порядок символов становится обратным.
 * @param {character[]} s
 * @return {void} Не возвращать ничего, изменить s на месте.
 */
var reverseString = function(s) {
    let i = 0, j = s.length - 1;
    while (i < j) {
        const tmp = s[i];
        s[i++] = s[j];
        s[j--] = tmp;
    }
};

// Альтернатива (короче, но создаёт новое значение при join/split — не in-place):
// const str = s.join('').split('').reverse(); // не рекомендовано если требуется in-place

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