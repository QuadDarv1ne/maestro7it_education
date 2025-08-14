/**
 * https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/
 */

using System;
using System.Collections.Generic;

/**
 * Генерирует все возможные комбинации букв для строки цифр digits.
 */
public class Solution {
    private string[] digitMap = {
        "", "", "abc", "def", "ghi", "jkl",
        "mno", "pqrs", "tuv", "wxyz"
    };

    public IList<string> LetterCombinations(string digits) {
        var result = new List<string>();
        if (string.IsNullOrEmpty(digits)) return result;
        Backtrack(digits, 0, "", result);
        return result;
    }

    private void Backtrack(string digits, int index, string current, List<string> result) {
        if (index == digits.Length) {
            result.Add(current);
            return;
        }
        string letters = digitMap[digits[index] - '0'];
        foreach (char c in letters) {
            Backtrack(digits, index + 1, current + c, result);
        }
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