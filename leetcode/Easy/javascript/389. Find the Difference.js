/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
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
 * @param {string} s
 * @param {string} t
 * @return {character}
 */
var findTheDifference = function(s, t) {
    // Создаём объект для подсчёта частот символов в s
    const count = {};

    // Подсчитываем каждый символ в s
    for (let ch of s) {
        count[ch] = (count[ch] || 0) + 1;
    }

    // Проходим по t и уменьшаем счётчики
    for (let ch of t) {
        if (count[ch]) {
            count[ch]--;
        } else {
            // Если символа нет в s или счётчик уже 0 — это добавленный символ
            return ch;
        }
    }

    // По условию задачи всегда должен найтись
    return '';
};