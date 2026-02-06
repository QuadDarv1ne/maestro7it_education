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
    /**
     * Находит максимальную разность между последовательными элементами в отсортированной форме.
     * Использует bucket sort для достижения O(n) времени.
     * 
     * Сложность по времени: O(n)
     * Сложность по памяти: O(n)
     */
    public int MaximumGap(int[] nums) {
        int n = nums.Length;
        if (n < 2) return 0;
        
        // Находим min и max
        int minVal = nums.Min();
        int maxVal = nums.Max();
        
        if (minVal == maxVal) return 0;
        
        // Размер корзины
        int bucketSize = Math.Max(1, (maxVal - minVal) / (n - 1));
        int bucketCount = (maxVal - minVal) / bucketSize + 1;
        
        // Инициализируем корзины [min, max]
        var buckets = new (int min, int max)[bucketCount];
        for (int i = 0; i < bucketCount; i++) {
            buckets[i] = (int.MaxValue, int.MinValue);
        }
        
        // Распределяем элементы по корзинам
        foreach (int num in nums) {
            int idx = (num - minVal) / bucketSize;
            buckets[idx].min = Math.Min(buckets[idx].min, num);
            buckets[idx].max = Math.Max(buckets[idx].max, num);
        }
        
        // Ищем максимальный gap между корзинами
        int maxGap = 0;
        int prevMax = minVal;
        
        foreach (var (bucketMin, bucketMax) in buckets) {
            if (bucketMin == int.MaxValue) {
                // Пустая корзина
                continue;
            }
            
            maxGap = Math.Max(maxGap, bucketMin - prevMax);
            prevMax = bucketMax;
        }
        
        return maxGap;
    }
}