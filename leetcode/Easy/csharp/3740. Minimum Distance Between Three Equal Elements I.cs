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
    /// Находит минимальное расстояние между тремя одинаковыми элементами в массиве.
    /// </summary>
    /// <remarks>
    /// Алгоритм группирует индексы вхождений каждого числа. 
    /// Для каждого числа, встречающегося минимум 3 раза, перебираются все комбинации 
    /// по 3 индекса. Расстояние вычисляется по формуле 2 * (k - i) для i &lt; j &lt; k.
    /// </remarks>
    /// <param name="nums">Входной массив целых чисел.</param>
    /// <returns>Минимальное расстояние или -1, если хороших троек не существует.</returns>
    public int MinimumDistance(int[] nums) {
        // Словарь для хранения списков индексов каждого числа
        var positions = new Dictionary<int, List<int>>();
        
        for (int i = 0; i < nums.Length; i++) {
            if (!positions.ContainsKey(nums[i])) {
                positions[nums[i]] = new List<int>();
            }
            positions[nums[i]].Add(i);
        }

        int minDist = int.MaxValue;

        foreach (var kvp in positions) {
            var idxList = kvp.Value;
            int n = idxList.Count;
            
            if (n < 3) continue;

            // Перебор всех троек (i, j, k)
            for (int i = 0; i < n - 2; i++) {
                for (int j = i + 1; j < n - 1; j++) {
                    for (int k = j + 1; k < n; k++) {
                        int dist = 2 * (idxList[k] - idxList[i]);
                        if (dist < minDist) {
                            minDist = dist;
                        }
                    }
                }
            }
        }

        return minDist == int.MaxValue ? -1 : minDist;
    }
}