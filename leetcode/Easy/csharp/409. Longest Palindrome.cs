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
    /// Возвращает длину самого длинного палиндрома, который можно составить.
    /// </summary>
    /// <param name="s">Исходная строка.</param>
    /// <returns>Максимальная длина палиндрома.</returns>
    public int LongestPalindrome(string s) {
        // Массив для подсчёта частот (ASCII 128)
        int[] freq = new int[128];

        foreach (char ch in s) {
            freq[ch]++;
        }

        int length = 0;
        bool oddExists = false;

        foreach (int count in freq) {
            length += (count / 2) * 2;
            if (count % 2 == 1) {
                oddExists = true;
            }
        }

        if (oddExists) {
            length += 1;
        }

        return length;
    }
}