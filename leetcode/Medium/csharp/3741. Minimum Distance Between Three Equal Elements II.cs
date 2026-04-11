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

/**
 * <summary>
 * Находит минимальное расстояние между тремя равными элементами в массиве.
 * </summary>
 * <param name="nums">Входной массив целых чисел.</param>
 * <returns>Минимальное расстояние или -1, если таких троек нет.</returns>
 * <remarks>
 * Алгоритм:
 * 1. Сгруппировать индексы по значениям элементов.
 * 2. Для каждого значения, где есть минимум 3 элемента, вычислить расстояние
 *    между первой и третьей позицией в каждой тройке последовательных индексов.
 * 3. Вернуть минимальное из найденных расстояний.
 * Сложность: O(n) по времени, O(n) по памяти.
 * </remarks>
 */
public class Solution {
    public int MinimumDistance(int[] nums) {
        var valueToIndices = new Dictionary<int, List<int>>();
        for (int i = 0; i < nums.Length; i++) {
            if (!valueToIndices.ContainsKey(nums[i])) {
                valueToIndices[nums[i]] = new List<int>();
            }
            valueToIndices[nums[i]].Add(i);
        }

        int minDist = int.MaxValue;
        foreach (var indices in valueToIndices.Values) {
            if (indices.Count >= 3) {
                for (int i = 0; i <= indices.Count - 3; i++) {
                    int dist = 2 * (indices[i + 2] - indices[i]);
                    if (dist < minDist) {
                        minDist = dist;
                    }
                }
            }
        }
        return minDist == int.MaxValue ? -1 : minDist;
    }
}