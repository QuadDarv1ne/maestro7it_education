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

class Solution {
public:
    /**
     * Вычисляет максимальную длину палиндрома из доступных букв.
     *
     * @param s строка с буквами (учёт регистра)
     * @return длина самого длинного палиндрома
     */
    int longestPalindrome(string s) {
        // Используем массив для ASCII (достаточно 128)
        vector<int> freq(128, 0);

        for (char ch : s) {
            freq[ch]++;
        }

        int length = 0;
        bool oddExists = false;

        for (int count : freq) {
            length += (count / 2) * 2;
            if (count % 2 == 1) {
                oddExists = true;
            }
        }

        if (oddExists) {
            length += 1;
        }

        return length;
    }
};