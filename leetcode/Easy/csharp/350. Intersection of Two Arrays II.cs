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
    /// Возвращает пересечение двух массивов с учётом кратности элементов.
    /// </summary>
    /// <param name="nums1">Первый массив целых чисел.</param>
    /// <param name="nums2">Второй массив целых чисел.</param>
    /// <returns>Массив общих элементов с повторениями.</returns>
    public int[] Intersect(int[] nums1, int[] nums2) {
        // Используем меньший массив для построения словаря частот
        if (nums1.Length > nums2.Length) {
            return Intersect(nums2, nums1);
        }
        
        var freq = new Dictionary<int, int>();
        foreach (int num in nums1) {
            if (freq.ContainsKey(num)) {
                freq[num]++;
            } else {
                freq[num] = 1;
            }
        }
        
        var resultList = new List<int>();
        foreach (int num in nums2) {
            if (freq.TryGetValue(num, out int count) && count > 0) {
                resultList.Add(num);
                freq[num] = count - 1;
            }
        }
        
        return resultList.ToArray();
    }
}