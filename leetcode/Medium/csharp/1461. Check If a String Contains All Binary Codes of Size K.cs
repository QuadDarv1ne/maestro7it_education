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

public class Solution {
    /// <summary>
    /// Проверяет, содержит ли строка s все бинарные коды длины k.
    /// </summary>
    /// <param name="s">входная бинарная строка</param>
    /// <param name="k">длина кода</param>
    /// <returns>true, если все коды присутствуют, иначе false</returns>
    public bool HasAllCodes(string s, int k) {
        int need = 1 << k;  // 2^k
        if (s.Length < need + k - 1) {
            return false;
        }
        
        var seen = new HashSet<string>();
        for (int i = 0; i <= s.Length - k; i++) {
            seen.Add(s.Substring(i, k));
            if (seen.Count == need) {
                return true;
            }
        }
        return seen.Count == need;
    }
}