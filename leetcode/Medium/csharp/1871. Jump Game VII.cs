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

public class Solution {
    /**
     * <summary>
     * Решение задачи Jump Game VII на C#.
     * 
     * Проверяет достижимость конца строки, двигаясь вперед прыжками
     * заданной длины и приземляясь только на '0'.
     * 
     * Поддерживается счетчик (count) достижимых предыдущих индексов в скользящем окне
     * [i - maxJump, i - minJump], что позволяет решать задачу за O(N).
     * </summary>
     * <param name="s">Бинарная строка.</param>
     * <param name="minJump">Минимальная длина прыжка.</param>
     * <param name="maxJump">Максимальная длина прыжка.</param>
     * <returns>True, если конец достижим, иначе False.</returns>
     */
    public bool CanReach(string s, int minJump, int maxJump) {
        int n = s.Length;
        bool[] dp = new bool[n];
        dp[0] = true;
        int count = 0;

        for (int i = 1; i < n; i++) {
            // Если индекс (i - minJump) достижим, добавляем его в окно
            if (i >= minJump && dp[i - minJump]) {
                count++;
            }
            // Если индекс (i - maxJump - 1) покидает окно, вычитаем его
            if (i > maxJump && dp[i - maxJump - 1]) {
                count--;
            }

            // Текущая позиция достижима, если это '0' и есть пути к ней (count > 0)
            if (s[i] == '0' && count > 0) {
                dp[i] = true;
            }
        }

        return dp[n - 1];
    }
}