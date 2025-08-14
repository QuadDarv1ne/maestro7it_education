/**
 * https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
 */

/**
 * Находит длину самой длинной подстроки без повторяющихся символов.
 *
 * Алгоритм:
 * - Используем метод скользящего окна (sliding window).
 * - lastSeen[c] хранит последний индекс символа c (или -1, если не встречался).
 * - Переменная j указывает на позицию перед началом текущего окна.
 * - Для каждого символа s.charAt(i):
 *     * Если символ уже встречался, сдвигаем j вправо (j = max(j, lastSeen[c])).
 *     * Вычисляем длину текущего окна: i - j.
 *     * Обновляем ответ (ans).
 *     * Запоминаем позицию символа (lastSeen[c] = i).
 *
 * Сложность:
 * - Время: O(n)
 * - Память: O(1) для ASCII.
 *
 * @param s входная строка
 * @return длина самой длинной подстроки без повторов
 */
class Solution {
    public int lengthOfLongestSubstring(String s) {
        int[] lastSeen = new int[128];
        java.util.Arrays.fill(lastSeen, -1);
        int ans = 0, j = -1;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (lastSeen[c] != -1) {
                j = Math.max(j, lastSeen[c]);
            }
            ans = Math.max(ans, i - j);
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