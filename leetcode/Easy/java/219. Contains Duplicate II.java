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

import java.util.HashMap;
import java.util.Map;

class Solution {
    public boolean containsNearbyDuplicate(int[] nums, int k) {
        // HashMap для хранения последнего индекса каждого числа
        Map<Integer, Integer> indexMap = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int num = nums[i];
            
            // Проверяем, встречалось ли число ранее
            if (indexMap.containsKey(num)) {
                // Проверяем разницу индексов
                if (i - indexMap.get(num) <= k) {
                    return true;
                }
            }
            
            // Обновляем индекс для текущего числа
            indexMap.put(num, i);
        }
        
        return false;
    }
}