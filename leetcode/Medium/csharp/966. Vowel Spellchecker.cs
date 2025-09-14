/**
 * https://leetcode.com/problems/vowel-spellchecker/description/?envType=daily-question&envId=2025-09-14
 */

using System;
using System.Collections.Generic;
using System.Linq;

public class Solution {
    /// <summary>
    /// Решение задачи Vowel Spellchecker.
    /// 
    /// Для каждого запроса из queries ищем слово в wordlist по следующим правилам:
    /// 1. Точное совпадение.
    /// 2. Совпадение без учета регистра (первое найденное).
    /// 3. Совпадение с заменой всех гласных на '*' (первое найденное).
    /// 4. Если ничего не найдено, возвращаем пустую строку.
    /// </summary>
    public string[] Spellchecker(string[] wordlist, string[] queries) {
        // Создаем множество для точных совпадений
        HashSet<string> exact = new HashSet<string>(wordlist);
        // Словарь для регистра-независимого поиска: ключ — слово в нижнем регистре, значение — первое слово из wordlist
        Dictionary<string, string> caseInsensitive = new Dictionary<string, string>();
        // Словарь для поиска с заменой гласных на '*': ключ — строка с замененными гласными, значение — первое слово
        Dictionary<string, string> vowelInsensitive = new Dictionary<string, string>();
        
        foreach (string word in wordlist) {
            string lower = word.ToLower();
            // Если в caseInsensitive еще нет этого ключа, добавляем
            if (!caseInsensitive.ContainsKey(lower)) {
                caseInsensitive[lower] = word;
            }
            // Заменяем гласные на * в lower
            char[] chars = lower.ToCharArray();
            for (int i = 0; i < chars.Length; i++) {
                if (chars[i] == 'a' || chars[i] == 'e' || chars[i] == 'i' || chars[i] == 'o' || chars[i] == 'u') {
                    chars[i] = '*';
                }
            }
            string vowelKey = new string(chars);
            if (!vowelInsensitive.ContainsKey(vowelKey)) {
                vowelInsensitive[vowelKey] = word;
            }
        }
        
        List<string> result = new List<string>();
        foreach (string query in queries) {
            // Проверяем точное совпадение
            if (exact.Contains(query)) {
                result.Add(query);
                continue;
            }
            string lowerQuery = query.ToLower();
            // Проверяем регистра-независимое совпадение
            if (caseInsensitive.ContainsKey(lowerQuery)) {
                result.Add(caseInsensitive[lowerQuery]);
                continue;
            }
            // Заменяем гласные на * в lowerQuery
            char[] chars = lowerQuery.ToCharArray();
            for (int i = 0; i < chars.Length; i++) {
                if (chars[i] == 'a' || chars[i] == 'e' || chars[i] == 'i' || chars[i] == 'o' || chars[i] == 'u') {
                    chars[i] = '*';
                }
            }
            string vowelQuery = new string(chars);
            if (vowelInsensitive.ContainsKey(vowelQuery)) {
                result.Add(vowelInsensitive[vowelQuery]);
            } else {
                result.Add("");
            }
        }
        return result.ToArray();
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/