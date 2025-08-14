/**
 * https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
 */

/// <summary>
/// Находит длину самой длинной подстроки без повторяющихся символов.
/// </summary>
/// <param name="s">Входная строка</param>
/// <returns>Длина самой длинной подстроки без повторов</returns>
/// <remarks>
/// Алгоритм:
/// - Используем метод скользящего окна (sliding window).
/// - lastSeen[c] хранит последний индекс символа c (или -1, если не встречался).
/// - Переменная j указывает на позицию перед началом текущего окна.
/// - Для каждого символа s[i]:
///     * Если символ уже встречался, сдвигаем j вправо.
///     * Вычисляем длину окна: i - j.
///     * Обновляем максимум.
///     * Запоминаем индекс текущего символа.
/// Время: O(n), Память: O(1) для ASCII.
/// </remarks>
public class Solution {
    public int LengthOfLongestSubstring(string s) {
        int[] lastSeen = new int[128];
        for (int k = 0; k < 128; k++) lastSeen[k] = -1;

        int ans = 0, j = -1;
        for (int i = 0; i < s.Length; i++) {
            char c = s[i];
            if (lastSeen[c] != -1) {
                j = Math.Max(j, lastSeen[c]);
            }
            ans = Math.Max(ans, i - j);
            lastSeen[c] = i;
        }
        return ans;
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