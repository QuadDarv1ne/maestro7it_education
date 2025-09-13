/**
 * https://leetcode.com/problems/find-most-frequent-vowel-and-consonant/description/?envType=daily-question&envId=2025-09-13
 */

using System;

/// <summary>
/// Задача: вернуть сумму максимальной частоты гласной и максимальной
/// частоты согласной в строке s.
/// 
/// Уточнения:
/// - Рассматриваются буквы 'a'..'z' и 'A'..'Z'.
/// - Гласные: a, e, i, o, u.
/// - Если гласных/согласных нет — вклад равен 0.
/// 
/// Сложность: O(n) по времени, O(1) по памяти.
/// </summary>
public class Solution {
    public int MaxFreqSum(string s) {
        int[] cnt = new int[26];
        foreach (char ch0 in s) {
            char ch = ch0;
            if (ch >= 'A' && ch <= 'Z') ch = (char)(ch - 'A' + 'a');
            if (ch >= 'a' && ch <= 'z') cnt[ch - 'a']++;
        }

        string vowels = "aeiou";
        int maxV = 0;
        foreach (char v in vowels) maxV = Math.Max(maxV, cnt[v - 'a']);

        int maxC = 0;
        for (int i = 0; i < 26; i++) {
            char ch = (char)('a' + i);
            if (vowels.IndexOf(ch) >= 0) continue;
            maxC = Math.Max(maxC, cnt[i]);
        }

        return maxV + maxC;
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