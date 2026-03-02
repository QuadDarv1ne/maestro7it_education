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
     * Находит добавленный символ с помощью разности сумм ASCII-кодов.
     *
     * @param s исходная строка
     * @param t строка с добавленным символом
     * @return добавленный символ
     */
    public char findTheDifference(String s, String t) {
        int sumS = 0, sumT = 0;

        // Суммируем ASCII-коды символов s
        for (int i = 0; i < s.length(); i++) {
            sumS += s.charAt(i);
        }

        // Суммируем ASCII-коды символов t
        for (int i = 0; i < t.length(); i++) {
            sumT += t.charAt(i);
        }

        // Разница сумм — ASCII-код добавленного символа
        return (char) (sumT - sumS);
    }
}