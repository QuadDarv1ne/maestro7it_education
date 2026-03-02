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
    /// Возвращает массив, где для каждого числа i от 0 до n указано
    /// количество единичных битов в его двоичном представлении.
    /// </summary>
    /// <param name="n">Верхняя граница диапазона.</param>
    /// <returns>Массив целых чисел длины n+1.</returns>
    public int[] CountBits(int n) {
        int[] ans = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            // Используем ранее вычисленное значение для числа i/2
            // и добавляем младший бит (0 для чётных, 1 для нечётных)
            ans[i] = ans[i >> 1] + (i & 1);
        }
        return ans;
    }
}