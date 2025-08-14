/**
 * https://leetcode.com/problems/valid-palindrome/description/
 */

/**
 * @param {string} s
 * @return {boolean}
 *
 * Проверяет, является ли s палиндромом, игнорируя небуквенно-цифровые символы и регистр.
 */
var isPalindrome = function(s) {
    let i = 0, j = s.length - 1;
    const isAlnum = ch => /[0-9a-zA-Z]/.test(ch);
    while (i < j) {
        while (i < j && !isAlnum(s[i])) i++;
        while (i < j && !isAlnum(s[j])) j--;
        if (i < j) {
            if (s[i].toLowerCase() !== s[j].toLowerCase()) return false;
            i++; j--;
        }
    }
    return true;
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