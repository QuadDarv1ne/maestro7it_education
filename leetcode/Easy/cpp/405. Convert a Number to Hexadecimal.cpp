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

class Solution {
public:
    /**
     * Преобразует 32-битное целое число в шестнадцатеричную строку.
     *
     * @param num входное целое число
     * @return шестнадцатеричное представление в нижнем регистре
     */
    string toHex(int num) {
        if (num == 0) return "0";

        // Интерпретируем int как беззнаковое 32-битное число
        unsigned int n = num;

        string hexChars = "0123456789abcdef";
        string result = "";

        while (n > 0) {
            int digit = n & 0xF;
            result = hexChars[digit] + result; // добавляем в начало
            n >>= 4;
        }

        return result;
    }
};