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

public class Solution {
    public bool ContainsNearbyDuplicate(int[] nums, int k) {
        // Словарь для хранения последнего индекса каждого числа
        Dictionary<int, int> indexMap = new Dictionary<int, int>();
        
        for (int i = 0; i < nums.Length; i++) {
            int num = nums[i];
            
            // Проверяем, есть ли число в словаре
            if (indexMap.ContainsKey(num)) {
                // Проверяем разницу индексов
                if (i - indexMap[num] <= k) {
                    return true;
                }
            }
            
            // Обновляем или добавляем индекс
            indexMap[num] = i;
        }
        
        return false;
    }
}