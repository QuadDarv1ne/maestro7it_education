/**
 * https://leetcode.com/problems/contains-duplicate-iii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "220. Contains Duplicate III"
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

import java.util.TreeSet;

class Solution {
    public boolean containsNearbyAlmostDuplicate(int[] nums, int k, int t) {
        if (k < 0 || t < 0) return false;
        
        TreeSet<Long> set = new TreeSet<>();
        
        for (int i = 0; i < nums.length; i++) {
            long current = nums[i];
            
            // Находим наименьший элемент ≥ current - t
            Long floor = set.floor(current + t);
            
            // Находим наибольший элемент ≤ current + t
            Long ceiling = set.ceiling(current - t);
            
            // Проверяем условия
            if ((floor != null && floor >= current - t) || 
                (ceiling != null && ceiling <= current + t)) {
                return true;
            }
            
            // Добавляем текущий элемент
            set.add(current);
            
            // Удаляем элемент, который выходит за пределы окна
            if (i >= k) {
                set.remove((long) nums[i - k]);
            }
        }
        
        return false;
    }
}