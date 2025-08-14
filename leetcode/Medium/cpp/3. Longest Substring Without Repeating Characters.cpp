/**
 * https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
 */

/**
 * @brief Находит длину самой длинной подстроки без повторяющихся символов.
 *
 * Алгоритм:
 * - Используем метод скользящего окна (sliding window).
 * - lastSeen[c] хранит последний индекс символа c (или -1, если не встречался).
 * - Переменная j указывает на позицию перед началом текущего окна.
 * - Для каждого символа s[i]:
 *     * Если символ уже встречался, сдвигаем j вправо (j = max(j, lastSeen[s[i]])).
 *     * Вычисляем длину текущего окна: i - j.
 *     * Обновляем ответ (ans).
 *     * Запоминаем позицию символа (lastSeen[s[i]] = i).
 *
 * Сложность:
 * - Время: O(n), где n — длина строки.
 * - Память: O(1) для фиксированного алфавита ASCII.
 *
 * @param s входная строка.
 * @return int длина самой длинной подстроки без повторяющихся символов.
 */
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        vector<int> lastSeen(128, -1);
        int ans = 0, j = -1;
        for (int i = 0; i < s.size(); i++) {
            if (lastSeen[s[i]] != -1) {
                j = max(j, lastSeen[s[i]]);
            }
            ans = max(ans, i - j);
            lastSeen[s[i]] = i;
        }
        return ans;
    }
};

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