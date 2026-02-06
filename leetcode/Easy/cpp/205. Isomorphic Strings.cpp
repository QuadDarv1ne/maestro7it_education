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

class Solution {
public:
    bool isIsomorphic(string s, string t) {
        if (s.length() != t.length()) return false;
        
        unordered_map<char, char> s_to_t;
        unordered_map<char, char> t_to_s;
        
        for (int i = 0; i < s.length(); i++) {
            char s_char = s[i];
            char t_char = t[i];
            
            // Проверяем s -> t
            if (s_to_t.find(s_char) != s_to_t.end()) {
                if (s_to_t[s_char] != t_char) return false;
            } else {
                s_to_t[s_char] = t_char;
            }
            
            // Проверяем t -> s
            if (t_to_s.find(t_char) != t_to_s.end()) {
                if (t_to_s[t_char] != s_char) return false;
            } else {
                t_to_s[t_char] = s_char;
            }
        }
        return true;
    }
};