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
    /// Возвращает минимальное количество изменений символов,
    /// чтобы строка стала чередующейся.
    /// </summary>
    /// <param name="s">Исходная строка из '0' и '1'</param>
    /// <returns>Минимальное число операций замены</returns>
    public int MinOperations(string s) {
        int n = s.Length;
        int count1 = 0; // несовпадения с паттерном, начинающимся с '0'
        int count2 = 0; // несовпадения с паттерном, начинающимся с '1'

        for (int i = 0; i < n; i++) {
            char c = s[i];
            // Паттерн1: чётные индексы '0', нечётные '1'
            if (i % 2 == 0 && c != '0') count1++;
            if (i % 2 == 1 && c != '1') count1++;

            // Паттерн2: чётные индексы '1', нечётные '0'
            if (i % 2 == 0 && c != '1') count2++;
            if (i % 2 == 1 && c != '0') count2++;
        }

        return Math.Min(count1, count2);
    }
}