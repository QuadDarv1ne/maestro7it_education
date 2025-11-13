/*
 * 3228. Maximum Number of Operations to Move Ones to the End
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * Источник идеи: LeetCode editorial / walkccc.
 */

public class Solution {
    public int MaxOperations(string s) {
        long ans = 0;
        long ones = 0;
        int n = s.Length;
        for (int i = 0; i < n; i++) {
            if (s[i] == '1') {
                ones++;
            } else if (i + 1 == n || s[i + 1] == '1') {
                ans += ones;
            }
        }
        return (int)ans;
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