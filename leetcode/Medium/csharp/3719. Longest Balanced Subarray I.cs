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
    /// Находит длину самого длинного сбалансированного подмассива.
    /// Подмассив сбалансирован, если количество уникальных четных чисел
    /// равно количеству уникальных нечетных чисел.
    /// </summary>
    /// <param name="nums">Входной массив целых чисел</param>
    /// <returns>Длина самого длинного сбалансированного подмассива</returns>
    /// <example>
    /// <code>
    /// LongestBalanced([2,5,4,3]) // возвращает 4
    /// LongestBalanced([3,2,2,5,4]) // возвращает 5
    /// LongestBalanced([1,2,3,2]) // возвращает 3
    /// </code>
    /// </example>
    public int LongestBalanced(int[] nums) {
        int n = nums.Length;
        int max_len = 0;
        
        for (int i = 0; i < n; i++) {
            HashSet<int> evenSet = new HashSet<int>();
            HashSet<int> oddSet = new HashSet<int>();
            
            for (int j = i; j < n; j++) {
                if (nums[j] % 2 == 0) {
                    evenSet.Add(nums[j]);
                } else {
                    oddSet.Add(nums[j]);
                }
                
                if (evenSet.Count == oddSet.Count) {
                    max_len = Math.Max(max_len, j - i + 1);
                }
            }
        }
        
        return max_len;
    }
}