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

import java.util.*;

class Solution {
    /**
     * Возвращает кратчайшее расстояние от startIndex до любого вхождения target
     * в циклическом массиве words. Если target отсутствует, возвращает -1.
     * 
     * @param words массив строк (циклический)
     * @param target искомая строка
     * @param startIndex начальный индекс
     * @return минимальное расстояние или -1
     */
    public int closestTarget(String[] words, String target, int startIndex) {
        int n = words.length;
        int minDist = Integer.MAX_VALUE;
        
        for (int i = 0; i < n; i++) {
            if (words[i].equals(target)) {
                // Расстояние по часовой стрелке (вправо)
                int clockwise = (i - startIndex + n) % n;
                // Расстояние против часовой стрелки (влево)
                int counterClockwise = (startIndex - i + n) % n;
                // Минимальное из двух направлений
                int dist = Math.min(clockwise, counterClockwise);
                minDist = Math.min(minDist, dist);
            }
        }
        
        return minDist == Integer.MAX_VALUE ? -1 : minDist;
    }
}