/**
 * https://leetcode.com/problems/maximum-number-of-words-you-can-type/description/?envType=daily-question&envId=2025-09-15
 */

using System;

public class Solution {
    /// <summary>
    /// Подсчитывает количество слов в тексте, которые можно набрать, не используя сломанные клавиши.
    /// </summary>
    /// <param name="text">Исходный текст, разделенный пробелами.</param>
    /// <param name="brokenLetters">Строка с символами сломанных клавиш.</param>
    /// <returns>Количество слов, которые можно набрать без использования сломанных клавиш.</returns>
    public int CanBeTypedWords(string text, string brokenLetters) {
        string[] words = text.Split(' ');
        int count = 0;
        foreach (string word in words) {
            bool valid = true;
            foreach (char c in word) {
                if (brokenLetters.Contains(c)) {
                    valid = false;
                    break;
                }
            }
            if (valid) {
                count++;
            }
        }
        return count;
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1  @quadd4rv1n7
# 3. Telegram №2  @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/