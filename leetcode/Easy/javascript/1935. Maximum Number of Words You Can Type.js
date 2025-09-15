/**
 * https://leetcode.com/problems/maximum-number-of-words-you-can-type/description/?envType=daily-question&envId=2025-09-15
 */

/**
 * Подсчитывает количество слов в тексте, которые можно набрать, не используя сломанные клавиши.
 * 
 * @param {string} text - Исходный текст, разделенный пробелами.
 * @param {string} brokenLetters - Строка с символами сломанных клавиш.
 * @returns {number} Количество слов, которые можно набрать без использования сломанных клавиш.
 */
var canBeTypedWords = function(text, brokenLetters) {
    const words = text.split(' ');
    let count = 0;
    for (const word of words) {
        let valid = true;
        for (const char of word) {
            if (brokenLetters.includes(char)) {
                valid = false;
                break;
            }
        }
        if (valid) {
            count++;
        }
    }
    return count;
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1  @quadd4rv1n7
# 3. Telegram №2  @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/