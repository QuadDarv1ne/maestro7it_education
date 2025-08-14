/**
 * https://leetcode.com/problems/zigzag-conversion/description/
 */

/// <summary>
/// Преобразует строку s в зигзагообразный паттерн с numRows строками.
/// </summary>
public class Solution {
    public string Convert(string s, int numRows) {
        if (numRows == 1 || numRows >= s.Length) return s;

        string[] rows = new string[numRows];
        for (int i = 0; i < numRows; i++) rows[i] = "";

        int currentRow = 0;
        bool goingDown = false;

        foreach (char c in s) {
            rows[currentRow] += c;
            if (currentRow == 0 || currentRow == numRows - 1)
                goingDown = !goingDown;
            currentRow += goingDown ? 1 : -1;
        }

        return string.Join("", rows);
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