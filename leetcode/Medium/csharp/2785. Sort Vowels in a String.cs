/**
 * https://leetcode.com/problems/sort-vowels-in-a-string/description/?envType=daily-question&envId=2025-09-11
 */

using System;
using System.Linq;
using System.Text;

public class Solution {
    /// <summary>
    /// Метод SortVowels принимает строку и сортирует все гласные буквы
    /// в порядке возрастания (по ASCII), оставляя остальные символы
    /// на своих местах.
    ///
    /// Алгоритм:
    /// 1. Собираем все гласные в список.
    /// 2. Сортируем их.
    /// 3. Подставляем обратно на места гласных.
    ///
    /// Временная сложность: O(n log n), где n — количество гласных.
    /// </summary>
    bool IsVowel(char c) {
        c = Char.ToLower(c);
        return "aeiou".Contains(c);
    }
    
    public string SortVowels(string s) {
        var vowels = s.Where(c => IsVowel(c)).ToList();
        vowels.Sort();
        int vi = 0;
        var result = new StringBuilder();
        foreach (char c in s) {
            if (IsVowel(c)) {
                result.Append(vowels[vi++]);
            } else {
                result.Append(c);
            }
        }
        return result.ToString();
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