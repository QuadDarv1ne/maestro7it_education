/**
 * Задача: Два лучших непересекающихся события (LeetCode #2054)
 * https://leetcode.com/problems/two-best-non-overlapping-events/
 * 
 * Описание:
 * Дан массив событий events, где events[i] = [startTime_i, endTime_i, value_i].
 * Каждое событие имеет время начала, время окончания и ценность.
 * Необходимо выбрать не более двух непересекающихся событий, чтобы максимизировать сумму их ценностей.
 * События не пересекаются, если конец первого события строго меньше начала второго (включительно: end < start).
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 * 
 * Сложность:
 * - Время: O(n log n) из-за сортировки и бинарного поиска
 * - Память: O(n) для хранения отсортированных массивов и префиксных максимумов
 */

import java.util.Arrays;

class Solution {
    /**
     * Находит максимальную сумму ценностей не более чем двух непересекающихся событий.
     * 
     * @param events int[][] - события в формате [начало, конец, ценность]
     * @return int - максимальная сумма ценностей
     * 
     * Автор: Дуплей Максим Игоревич
     * ORCID: https://orcid.org/0009-0007-7605-539X
     * GitHub: https://github.com/QuadDarv1ne/
     */
    public int maxTwoEvents(int[][] events) {
        int n = events.length;
        
        // Сортируем события по времени окончания
        int[][] eventsByEnd = events.clone();
        Arrays.sort(eventsByEnd, (a, b) -> Integer.compare(a[1], b[1]));
        
        // Создаем массивы времен окончания и префиксных максимумов
        int[] endTimes = new int[n];
        int[] prefixMax = new int[n];
        
        for (int i = 0; i < n; i++) {
            endTimes[i] = eventsByEnd[i][1];
            if (i == 0) {
                prefixMax[i] = eventsByEnd[i][2];
            } else {
                prefixMax[i] = Math.max(prefixMax[i-1], eventsByEnd[i][2]);
            }
        }
        
        // Находим максимальную ценность одного события
        int maxValue = 0;
        for (int[] event : events) {
            maxValue = Math.max(maxValue, event[2]);
        }
        
        // Перебираем каждое событие как второе
        for (int[] event : events) {
            int start = event[0];
            int value = event[2];
            
            // Бинарный поиск последнего события, которое заканчивается до start
            int idx = binarySearch(endTimes, start) - 1;
            
            if (idx >= 0) {
                maxValue = Math.max(maxValue, prefixMax[idx] + value);
            }
        }
        
        return maxValue;
    }
    
    /**
     * Вспомогательный метод для бинарного поиска
     * Возвращает индекс первого элемента >= target
     */
    private int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        return left;
    }
}