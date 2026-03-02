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

public class Solution {
    /// <summary>
    /// Преобразует 32-битное целое число в шестнадцатеричную строку.
    /// </summary>
    /// <param name="num">Входное целое число.</param>
    /// <returns>Шестнадцатеричное представление в нижнем регистре.</returns>
    public string ToHex(int num) {
        if (num == 0) return "0";

        // Интерпретируем int как беззнаковое 32-битное число
        uint n = (uint)num;

        char[] hexChars = "0123456789abcdef".ToCharArray();
        var result = new System.Text.StringBuilder();

        while (n > 0) {
            uint digit = n & 0xF;
            result.Append(hexChars[digit]);
            n >>= 4;
        }

        // Разворачиваем строку, так как собирали от младших битов
        return new string(result.ToString().Reverse().ToArray());
    }
}