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
    public bool WordPattern(string pattern, string s) {
        string[] words = s.Split(' ');
        if (pattern.Length != words.Length) return false;

        var charToWord = new Dictionary<char, string>();
        var wordToChar = new Dictionary<string, char>();

        for (int i = 0; i < pattern.Length; i++) {
            char ch = pattern[i];
            string word = words[i];

            if (charToWord.ContainsKey(ch)) {
                // Проверяем, что символ уже сопоставлен с этим словом
                if (charToWord[ch] != word) return false;
            } else {
                // Проверяем, не сопоставлено ли слово другому символу
                if (wordToChar.ContainsKey(word)) return false;
                // Добавляем новые сопоставления
                charToWord[ch] = word;
                wordToChar[word] = ch;
            }
        }
        return true;
    }
}