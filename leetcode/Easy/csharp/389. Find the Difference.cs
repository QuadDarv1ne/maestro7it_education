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
    /// Находит добавленный символ с помощью массива частот.
    /// </summary>
    /// <param name="s">Исходная строка.</param>
    /// <param name="t">Строка с добавленным символом.</param>
    /// <returns>Добавленный символ.</returns>
    public char FindTheDifference(string s, string t) {
        // Массив для подсчёта 26 строчных букв
        int[] count = new int[26];

        // Увеличиваем счётчики для символов s
        foreach (char ch in s) {
            count[ch - 'a']++;
        }

        // Уменьшаем счётчики для символов t
        foreach (char ch in t) {
            int index = ch - 'a';
            count[index]--;
            // Если счётчик ушёл в минус — это добавленный символ
            if (count[index] < 0) {
                return ch;
            }
        }

        // По условию задачи всегда должен найтись
        return ' ';
    }
}