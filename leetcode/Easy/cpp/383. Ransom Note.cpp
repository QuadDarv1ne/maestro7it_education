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
     * Проверяет, можно ли составить строку ransomNote из букв magazine.
     *
     * @param ransomNote целевая строка
     * @param magazine   строка-источник букв
     * @return true, если составить можно, иначе false
     */
    bool canConstruct(string ransomNote, string magazine) {
        // Массив счётчиков для 26 букв
        int count[26] = {0};

        // Подсчитываем буквы в magazine
        for (char ch : magazine) {
            count[ch - 'a']++;
        }

        // Проверяем ransomNote
        for (char ch : ransomNote) {
            int index = ch - 'a';
            count[index]--;
            if (count[index] < 0) {
                return false;
            }
        }

        return true;
    }
};