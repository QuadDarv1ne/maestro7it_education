/**
 * https://leetcode.com/problems/the-skyline-problem/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "218. The Skyline Problem"
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
    public List<List<Integer>> getSkyline(int[][] buildings) {
        List<List<Integer>> result = new ArrayList<>();
        if (buildings == null || buildings.length == 0) {
            return result;
        }
        
        // Создаем список событий
        List<int[]> events = new ArrayList<>();
        for (int[] building : buildings) {
            int left = building[0];
            int right = building[1];
            int height = building[2];
            
            // Начало здания - отрицательная высота
            events.add(new int[]{left, -height});
            // Конец здания - положительная высота
            events.add(new int[]{right, height});
        }
        
        // Сортируем события
        events.sort((a, b) -> {
            if (a[0] != b[0]) {
                return Integer.compare(a[0], b[0]);
            }
            // При одинаковом X: начала обрабатываем до концов
            return Integer.compare(a[1], b[1]);
        });
        
        // Максимальная куча для хранения текущих высот
        // PriorityQueue в Java - min-heap, поэтому используем обратный компаратор
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        maxHeap.offer(0);  // Уровень земли
        
        // Для отслеживания активных высот
        Map<Integer, Integer> heightCount = new HashMap<>();
        heightCount.put(0, 1);
        
        // Предыдущая максимальная высота
        int prevMax = 0;
        
        // Обрабатываем события
        for (int[] event : events) {
            int x = event[0];
            int height = event[1];
            
            if (height < 0) {
                // Начало здания
                height = -height;
                maxHeap.offer(height);
                heightCount.put(height, heightCount.getOrDefault(height, 0) + 1);
            } else {
                // Конец здания
                heightCount.put(height, heightCount.get(height) - 1);
            }
            
            // Удаляем неактивные высоты из кучи
            while (!maxHeap.isEmpty() && heightCount.get(maxHeap.peek()) == 0) {
                maxHeap.poll();
            }
            
            // Текущая максимальная высота
            int currentMax = maxHeap.peek();
            
            // Если высота изменилась
            if (currentMax != prevMax) {
                result.add(Arrays.asList(x, currentMax));
                prevMax = currentMax;
            }
        }
        
        return result;
    }
}