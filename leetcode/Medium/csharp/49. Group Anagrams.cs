/**
 * https://leetcode.com/problems/group-anagrams/description/
 */

using System.Collections.Generic;

public class Solution {
    public IList<IList<string>> GroupAnagrams(string[] strs) {
        var dict = new Dictionary<string, List<string>>();
        foreach (var s in strs) {
            var arr = s.ToCharArray();
            Array.Sort(arr);
            var key = new string(arr);
            if (!dict.ContainsKey(key)) dict[key] = new List<string>();
            dict[key].Add(s);
        }
        return new List<IList<string>>(dict.Values);
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/