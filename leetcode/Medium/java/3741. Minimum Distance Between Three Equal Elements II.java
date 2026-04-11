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

/**
 * Класс для решения задачи поиска минимального расстояния между тремя равными элементами.
 */
class Solution {
    /**
     * Находит минимальное расстояние между тремя равными элементами в массиве.
     *
     * Алгоритм:
     * 1. Сгруппировать индексы каждого числа с помощью HashMap.
     * 2. Для каждой группы, содержащей >=3 элемента, вычислить расстояние как
     *    2 * (третий индекс - первый индекс) для всех троек последовательных индексов.
     * 3. Вернуть минимальное найденное расстояние или -1, если таких троек нет.
     *
     * @param nums массив целых чисел
     * @return минимальное расстояние или -1
     */
    public int minimumDistance(int[] nums) {
        Map<Integer, List<Integer>> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            map.computeIfAbsent(nums[i], k -> new ArrayList<>()).add(i);
        }

        int minDist = Integer.MAX_VALUE;
        for (List<Integer> indices : map.values()) {
            if (indices.size() >= 3) {
                for (int i = 0; i <= indices.size() - 3; i++) {
                    int dist = 2 * (indices.get(i + 2) - indices.get(i));
                    minDist = Math.min(minDist, dist);
                }
            }
        }
        return minDist == Integer.MAX_VALUE ? -1 : minDist;
    }
}