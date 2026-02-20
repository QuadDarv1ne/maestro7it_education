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
     * Подсчитывает количество специальных подстрок в двоичной строке.
     *
     * @param s Бинарная строка, состоящая только из '0' и '1'.
     * @return Количество подстрок с равным числом сгруппированных 0 и 1.
     *
     * Пример:
     *   new Solution().countBinarySubstrings("00110011") → 6
     */
    public int countBinarySubstrings(String s) {
        int prevCount = 0;   // Длина предыдущей группы
        int currCount = 1;   // Длина текущей группы
        int result = 0;

        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == s.charAt(i - 1)) {
                currCount++;          // Продолжаем текущую группу
            } else {
                result += Math.min(prevCount, currCount); // Добавляем минимум на границе
                prevCount = currCount;
                currCount = 1;
            }
        }
        // Последняя граница
        result += Math.min(prevCount, currCount);
        return result;
    }
}