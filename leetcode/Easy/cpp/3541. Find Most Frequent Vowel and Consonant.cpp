/**
 * https://leetcode.com/problems/find-most-frequent-vowel-and-consonant/description/?envType=daily-question&envId=2025-09-13
 */

class Solution {
public:
    /**
     * Задача: вернуть сумму максимальной частоты гласной и максимальной
     * частоты согласной в строке s.
     *
     * Уточнения:
     * - Рассматриваются только латинские буквы 'a'..'z' (LeetCode даёт нижний регистр).
     * - Гласные: a, e, i, o, u.
     * - Если гласных/согласных нет — вклад равен 0.
     *
     * Сложность: O(n) по времени, O(1) по памяти.
     */
    int maxFreqSum(string s) {
        vector<int> cnt(26, 0);
        for (char c : s) {
            if ('a' <= c && c <= 'z') ++cnt[c - 'a'];
            else {
                char lc = tolower((unsigned char)c);
                if ('a' <= lc && lc <= 'z') ++cnt[lc - 'a'];
            }
        }
        string vowels = "aeiou";
        int maxV = 0, maxC = 0;
        for (char v : vowels) maxV = max(maxV, cnt[v - 'a']);
        for (int i = 0; i < 26; ++i) {
            char ch = 'a' + i;
            if (vowels.find(ch) != string::npos) continue;
            maxC = max(maxC, cnt[i]);
        }
        return maxV + maxC;
    }
};

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