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
    /// Определяет, можно ли составить строку ransomNote из букв magazine.
    /// </summary>
    /// <param name="ransomNote">Строка для составления.</param>
    /// <param name="magazine">Строка с доступными буквами.</param>
    /// <returns>true, если можно составить; иначе false.</returns>
    public bool CanConstruct(string ransomNote, string magazine) {
        // Массив для подсчёта 26 строчных букв
        int[] count = new int[26];

        // Подсчёт букв в magazine
        foreach (char ch in magazine) {
            count[ch - 'a']++;
        }

        // Проверка наличия букв для ransomNote
        foreach (char ch in ransomNote) {
            int index = ch - 'a';
            count[index]--;
            if (count[index] < 0) {
                return false;
            }
        }

        return true;
    }
}