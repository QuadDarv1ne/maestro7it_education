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
     * Находит минимальное кольцевое расстояние до ДРУГОГО равного элемента.
     *
     * @param nums   Исходный кольцевой массив.
     * @param queries Запросы индексов.
     * @return Список с минимальными расстояниями (-1 если элемент уникален).
     */
    public List<Integer> solveQueries(int[] nums, int[] queries) {
        int n = nums.length;
        // Карта: Значение -> Список индексов, где оно встречается
        Map<Integer, List<Integer>> indexMap = new HashMap<>();
        
        // 1. Построение карты индексов
        for (int i = 0; i < n; i++) {
            indexMap.computeIfAbsent(nums[i], k -> new ArrayList<>()).add(i);
        }
        
        List<Integer> answer = new ArrayList<>();
        
        // 2. Обработка запросов
        for (int q : queries) {
            int val = nums[q];
            List<Integer> pos = indexMap.get(val);
            int m = pos.size();
            
            // Если значение встречается только один раз
            if (m == 1) {
                answer.add(-1);
                continue;
            }
            
            // Бинарный поиск позиции q в списке индексов pos
            // Поскольку q точно есть в списке, binarySearch вернет >= 0
            int idx = Collections.binarySearch(pos, q);
            
            // Индексы соседей в списке pos (с учетом закольцованности)
            int leftIdx = (idx - 1 + m) % m;
            int rightIdx = (idx + 1) % m;
            
            int leftPos = pos.get(leftIdx);
            int rightPos = pos.get(rightIdx);
            
            // Вычисление кольцевого расстояния до левого соседа
            int dLeft = Math.abs(q - leftPos);
            int distLeft = Math.min(dLeft, n - dLeft);
            
            // Вычисление кольцевого расстояния до правого соседа
            int dRight = Math.abs(q - rightPos);
            int distRight = Math.min(dRight, n - dRight);
            
            // Добавляем минимальное из двух расстояний
            answer.add(Math.min(distLeft, distRight));
        }
        
        return answer;
    }
}