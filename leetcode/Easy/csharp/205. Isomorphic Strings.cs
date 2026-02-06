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
    public bool IsIsomorphic(string s, string t) {
        if (s.Length != t.Length) return false;
        
        Dictionary<char, char> sToT = new Dictionary<char, char>();
        Dictionary<char, char> tToS = new Dictionary<char, char>();
        
        for (int i = 0; i < s.Length; i++) {
            char sChar = s[i];
            char tChar = t[i];
            
            // Используем TryGetValue для оптимизации
            if (sToT.TryGetValue(sChar, out char mappedT)) {
                if (mappedT != tChar) return false;
            } else {
                sToT[sChar] = tChar;
            }
            
            if (tToS.TryGetValue(tChar, out char mappedS)) {
                if (mappedS != sChar) return false;
            } else {
                tToS[tChar] = sChar;
            }
        }
        
        return true;
    }
}