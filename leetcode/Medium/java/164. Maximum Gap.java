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

class Solution {
    /**
     * Находит максимальную разность между последовательными элементами в отсортированной форме.
     * Использует bucket sort для достижения O(n) времени.
     * 
     * Сложность по времени: O(n)
     * Сложность по памяти: O(n)
     */
    public int maximumGap(int[] nums) {
        int n = nums.length;
        if (n < 2) return 0;
        
        // Находим min и max
        int minVal = Arrays.stream(nums).min().getAsInt();
        int maxVal = Arrays.stream(nums).max().getAsInt();
        
        if (minVal == maxVal) return 0;
        
        // Размер корзины
        int bucketSize = Math.max(1, (maxVal - minVal) / (n - 1));
        int bucketCount = (maxVal - minVal) / bucketSize + 1;
        
        // Инициализируем корзины [min, max]
        int[][] buckets = new int[bucketCount][2];
        for (int i = 0; i < bucketCount; i++) {
            buckets[i][0] = Integer.MAX_VALUE;
            buckets[i][1] = Integer.MIN_VALUE;
        }
        
        // Распределяем элементы по корзинам
        for (int num : nums) {
            int idx = (num - minVal) / bucketSize;
            buckets[idx][0] = Math.min(buckets[idx][0], num);
            buckets[idx][1] = Math.max(buckets[idx][1], num);
        }
        
        // Ищем максимальный gap между корзинами
        int maxGap = 0;
        int prevMax = minVal;
        
        for (int[] bucket : buckets) {
            if (bucket[0] == Integer.MAX_VALUE) {
                // Пустая корзина
                continue;
            }
            
            maxGap = Math.max(maxGap, bucket[0] - prevMax);
            prevMax = bucket[1];
        }
        
        return maxGap;
    }
}