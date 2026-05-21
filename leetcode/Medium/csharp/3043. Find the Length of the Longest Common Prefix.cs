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

using System;
using System.Collections.Generic;

public class Solution {
    public int LongestCommonPrefix(int[] arr1, int[] arr2) {
        /*
         * Находит длину самого длинного общего префикса среди всех пар (x, y).
         * Использует HashSet для хранения всех префиксов arr1.
         */
        HashSet<int> prefixes = new HashSet<int>();

        // Собираем все префиксы чисел из arr1
        foreach (int x in arr1) {
            int num = x;
            while (num > 0) {
                prefixes.Add(num);
                num /= 10;
            }
        }

        int maxLen = 0;

        // Проверяем префиксы чисел из arr2
        foreach (int y in arr2) {
            int num = y;
            while (num > 0) {
                if (prefixes.Contains(num)) {
                    maxLen = Math.Max(maxLen, num.ToString().Length);
                    break; // Нашли самый длинный префикс для этого числа
                }
                num /= 10;
            }
        }

        return maxLen;
    }
}