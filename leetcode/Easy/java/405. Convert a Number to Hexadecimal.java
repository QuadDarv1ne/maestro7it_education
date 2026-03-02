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
    /**
     * Преобразует 32-битное целое число в шестнадцатеричную строку.
     *
     * @param num входное целое число
     * @return шестнадцатеричное представление в нижнем регистре
     */
    public String toHex(int num) {
        if (num == 0) return "0";

        // Используем long для промежуточных вычислений, чтобы избежать переполнения
        long n = num & 0x00000000ffffffffL; // интерпретируем как беззнаковое 32-битное

        char[] hexChars = "0123456789abcdef".toCharArray();
        StringBuilder result = new StringBuilder();

        while (n > 0) {
            int digit = (int)(n & 0xF);
            result.append(hexChars[digit]);
            n >>= 4;
        }

        // Разворачиваем, так как собирали от младших к старшим
        return result.reverse().toString();
    }
}