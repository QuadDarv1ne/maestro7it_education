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

public class Solution {
    /// <summary>
    /// Возвращает n-е уродливое число.
    /// Уродливые числа — положительные числа, простые множители которых
    /// ограничены 2, 3 и 5.
    /// </summary>
    /// <param name="n">Порядковый номер уродливого числа (1-индексировано)</param>
    /// <returns>n-е уродливое число</returns>
    /// <example>
    /// <code>
    /// NthUglyNumber(10) // возвращает 12
    /// NthUglyNumber(1)  // возвращает 1
    /// </code>
    /// </example>
    /// <remarks>
    /// Сложность:
    ///   Время: O(n)
    ///   Память: O(n)
    /// </remarks>
    public int NthUglyNumber(int n) {
        int[] ugly = new int[n];
        ugly[0] = 1;
        int i2 = 0, i3 = 0, i5 = 0;
        int next2 = 2, next3 = 3, next5 = 5;
        
        for (int i = 1; i < n; i++) {
            ugly[i] = Math.Min(next2, Math.Min(next3, next5));
            
            if (ugly[i] == next2) {
                i2++;
                next2 = ugly[i2] * 2;
            }
            if (ugly[i] == next3) {
                i3++;
                next3 = ugly[i3] * 3;
            }
            if (ugly[i] == next5) {
                i5++;
                next5 = ugly[i5] * 5;
            }
        }
        
        return ugly[n - 1];
    }
}