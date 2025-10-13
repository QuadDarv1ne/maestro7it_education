/*
https://leetcode.com/problems/find-resultant-array-after-removing-anagrams/  

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
*/

using System;
using System.Collections.Generic;
using System.Linq;

public class Solution {
    public IList<string> RemoveAnagrams(string[] words) {
        var result = new List<string>();
        string prev = "";
        foreach (var word in words) {
            string sorted = String.Concat(word.OrderBy(c => c));
            if (sorted != prev) {
                result.Add(word);
                prev = sorted;
            }
        }
        return result;
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
# 8. Официальный сайт школы Maestro7IT: https://school-maestro7it.ru/  
*/