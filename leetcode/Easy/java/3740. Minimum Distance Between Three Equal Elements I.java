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
     * Находит минимальное расстояние между тремя одинаковыми элементами в массиве.
     *
     * Метод группирует позиции каждого числа в HashMap.
     * Для чисел, имеющих хотя бы 3 вхождения, перебираются все комбинации индексов (i, j, k).
     * Искомое расстояние равно 2 * (k - i), так как i < j < k.
     *
     * @param nums входной массив целых чисел.
     * @return минимальное расстояние или -1, если нет троек с одинаковыми элементами.
     */
    public int minimumDistance(int[] nums) {
        // 1. Сбор индексов для каждого уникального значения
        Map<Integer, List<Integer>> positions = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            positions.computeIfAbsent(nums[i], k -> new ArrayList<>()).add(i);
        }

        int minDist = Integer.MAX_VALUE;

        // 2. Обработка каждого значения
        for (Map.Entry<Integer, List<Integer>> entry : positions.entrySet()) {
            List<Integer> idxList = entry.getValue();
            int n = idxList.size();
            
            if (n < 3) continue;

            // 3. Поиск минимальной разницы между крайними элементами тройки
            for (int i = 0; i < n - 2; i++) {
                for (int j = i + 1; j < n - 1; j++) {
                    for (int k = j + 1; k < n; k++) {
                        int dist = 2 * (idxList.get(k) - idxList.get(i));
                        minDist = Math.min(minDist, dist);
                    }
                }
            }
        }

        return minDist == Integer.MAX_VALUE ? -1 : minDist;
    }
}