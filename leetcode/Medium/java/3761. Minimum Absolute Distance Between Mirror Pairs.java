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
    /**
     * Находит минимальное расстояние между зеркальными парами в массиве.
     *
     * @param nums Исходный массив целых чисел.
     * @return Минимальная разница индексов |i - j| или -1, если пар нет.
     */
    public int minMirrorPairDistance(int[] nums) {
        int minDist = Integer.MAX_VALUE;
        Map<Integer, Integer> lastSeen = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int val = nums[i];
            
            // 1. Проверяем, не является ли val перевертышем ранее встреченного числа
            if (lastSeen.containsKey(val)) {
                int dist = i - lastSeen.get(val);
                if (dist < minDist) {
                    minDist = dist;
                }
            }
            
            // 2. Переворачиваем val и сохраняем индекс
            String reversedStr = new StringBuilder(String.valueOf(val)).reverse().toString();
            int rev = Integer.parseInt(reversedStr);
            
            lastSeen.put(rev, i);
        }
        
        return minDist == Integer.MAX_VALUE ? -1 : minDist;
    }
}