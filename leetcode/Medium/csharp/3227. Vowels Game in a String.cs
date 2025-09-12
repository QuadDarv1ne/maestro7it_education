/**
 * https://leetcode.com/problems/vowels-game-in-a-string/description/?envType=daily-question&envId=2025-09-12
 */

public class Solution {
    /// <summary>
    /// Определяет, выиграет ли Alice в игре "Vowels Game in a String".
    /// Alice выигрывает тогда и только тогда, когда в строке есть хотя бы одна гласная (a, e, i, o, u).
    /// Если гласных нет — она не может сделать первый ход и проигрывает.
    ///
    /// Временная сложность: O(n), где n — длина строки.
    /// Дополнительная память: O(1).
    /// </summary>
    public bool DoesAliceWin(string s) {
        foreach (char c in s) {
            if ("aeiou".Contains(c)) {
                return true;
            }
        }
        return false;
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