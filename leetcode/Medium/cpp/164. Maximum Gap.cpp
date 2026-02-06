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
public:
    /**
     * Находит максимальную разность между последовательными элементами в отсортированной форме.
     * Использует bucket sort для достижения O(n) времени.
     * 
     * Сложность по времени: O(n)
     * Сложность по памяти: O(n)
     */
    int maximumGap(vector<int>& nums) {
        int n = nums.size();
        if (n < 2) return 0;
        
        // Находим min и max
        int minVal = *min_element(nums.begin(), nums.end());
        int maxVal = *max_element(nums.begin(), nums.end());
        
        if (minVal == maxVal) return 0;
        
        // Размер корзины
        int bucketSize = max(1, (maxVal - minVal) / (n - 1));
        int bucketCount = (maxVal - minVal) / bucketSize + 1;
        
        // Инициализируем корзины [min, max]
        vector<pair<int, int>> buckets(bucketCount, {INT_MAX, INT_MIN});
        
        // Распределяем элементы по корзинам
        for (int num : nums) {
            int idx = (num - minVal) / bucketSize;
            buckets[idx].first = min(buckets[idx].first, num);
            buckets[idx].second = max(buckets[idx].second, num);
        }
        
        // Ищем максимальный gap между корзинами
        int maxGap = 0;
        int prevMax = minVal;
        
        for (auto& [bucketMin, bucketMax] : buckets) {
            if (bucketMin == INT_MAX) {
                // Пустая корзина
                continue;
            }
            
            maxGap = max(maxGap, bucketMin - prevMax);
            prevMax = bucketMax;
        }
        
        return maxGap;
    }
};