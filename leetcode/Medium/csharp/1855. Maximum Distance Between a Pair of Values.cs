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
    /// Находит максимальное расстояние между валидной парой индексов (i, j),
    /// где i <= j и nums1[i] <= nums2[j].
    /// </summary>
    /// <param name="nums1">первый невозрастающий массив</param>
    /// <param name="nums2">второй невозрастающий массив</param>
    /// <returns>максимальное расстояние (j - i) или 0</returns>
    public int MaxDistance(int[] nums1, int[] nums2) {
        int i = 0, j = 0, maxDist = 0;
        
        while (i < nums1.Length && j < nums2.Length) {
            if (nums1[i] <= nums2[j]) {
                if (i <= j) {
                    maxDist = Math.Max(maxDist, j - i);
                }
                j++;
            } else {
                i++;
            }
        }
        return maxDist;
    }
}