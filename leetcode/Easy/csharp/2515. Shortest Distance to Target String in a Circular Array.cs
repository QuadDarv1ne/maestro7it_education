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
    /// <summary>
    /// Возвращает кратчайшее расстояние от startIndex до любого вхождения target
    /// в циклическом массиве words. Если target отсутствует, возвращает -1.
    /// </summary>
    /// <param name="words">массив строк (циклический)</param>
    /// <param name="target">искомая строка</param>
    /// <param name="startIndex">начальный индекс</param>
    /// <returns>минимальное расстояние или -1</returns>
    public int ClosestTarget(string[] words, string target, int startIndex) {
        int n = words.Length;
        int minDist = int.MaxValue;
        
        for (int i = 0; i < n; i++) {
            if (words[i] == target) {
                // Расстояние по часовой стрелке (вправо)
                int clockwise = (i - startIndex + n) % n;
                // Расстояние против часовой стрелки (влево)
                int counterClockwise = (startIndex - i + n) % n;
                // Минимальное из двух направлений
                int dist = Math.Min(clockwise, counterClockwise);
                minDist = Math.Min(minDist, dist);
            }
        }
        
        return minDist == int.MaxValue ? -1 : minDist;
    }
}