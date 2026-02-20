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

using System;
using System.Collections.Generic;
using System.Linq;

public class Solution {
    /// <summary>
    /// Преобразует специальную двоичную строку в лексикографически наибольшую.
    /// </summary>
    /// <param name="s">Исходная специальная строка (например, "11011000")</param>
    /// <returns>Максимально возможная строка после перестановок (например, "11100100")</returns>
    public string MakeLargestSpecial(string s) {
        return Dfs(s);
    }
    
    private string Dfs(string s) {
        if (string.IsNullOrEmpty(s)) return "";
        
        var groups = new List<string>();
        int balance = 0;
        int left = 0;
        
        for (int i = 0; i < s.Length; i++) {
            balance += s[i] == '1' ? 1 : -1;
            if (balance == 0) {
                // Рекурсивно обрабатываем внутренность между первым и последним символом
                string inner = Dfs(s.Substring(left + 1, i - left - 1));
                groups.Add("1" + inner + "0");
                left = i + 1;
            }
        }
        
        // Сортируем группы по убыванию (лексикографически)
        groups.Sort((a, b) => b.CompareTo(a));
        return string.Concat(groups);
    }
}