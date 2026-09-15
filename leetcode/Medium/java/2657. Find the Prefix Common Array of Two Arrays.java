/**
 * https://leetcode.com/problems/house-robber-ii/description/
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
    public int[] findThePrefixCommonArray(int[] A, int[] B) {
        /*
         * Возвращает префиксный массив общих элементов C для двух перестановок A и B.
         * Используем массив счётчиков: когда число встретилось 2 раза,
         * оно становится общим.
         */
        int n = A.length;
        int[] count = new int[n + 1];
        int[] result = new int[n];
        int common = 0;

        for (int i = 0; i < n; i++) {
            count[A[i]]++;
            if (count[A[i]] == 2) common++;

            count[B[i]]++;
            if (count[B[i]] == 2) common++;

            result[i] = common;
        }

        return result;
    }
}