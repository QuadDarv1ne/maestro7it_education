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
    /**
     * Проверяет, можно ли составить ransomNote из букв magazine.
     *
     * @param ransomNote строка, которую нужно составить
     * @param magazine   строка с доступными буквами
     * @return true, если можно составить, иначе false
     */
    public boolean canConstruct(String ransomNote, String magazine) {
        // Массив для подсчёта 26 строчных букв
        int[] count = new int[26];

        // Подсчёт букв в magazine
        for (char ch : magazine.toCharArray()) {
            count[ch - 'a']++;
        }

        // Проверка наличия букв для ransomNote
        for (char ch : ransomNote.toCharArray()) {
            int index = ch - 'a';
            count[index]--;
            if (count[index] < 0) {
                return false;
            }
        }

        return true;
    }
}