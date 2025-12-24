/**
 * Задача: Два лучших непересекающихся события (LeetCode #2054)
 * 
 * Описание:
 * Дан массив событий events, где events[i] = [startTime_i, endTime_i, value_i].
 * Каждое событие имеет время начала, время окончания и ценность.
 * Необходимо выбрать не более двух непересекающихся событий, чтобы максимизировать сумму их ценностей.
 * События не пересекаются, если конец первого события строго меньше начала второго (включительно: end < start).
 * 
 * Автор: Дуплей Максим Игоревич
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
 * 
 * Сложность:
 * - Время: O(n log n) - сортировка + бинарный поиск для каждого события
 * - Память: O(n) для хранения отсортированных массивов и префиксных максимумов
 */

using System;
using System.Linq;

public class Solution {
    public int MaxTwoEvents(int[][] events) {
        int n = events.Length;
        
        // Сортируем события по времени окончания
        var eventsByEnd = events.OrderBy(e => e[1]).ToArray();
        
        // Создаем массивы времен окончания и префиксных максимумов
        int[] endTimes = new int[n];
        int[] prefixMax = new int[n];
        
        for (int i = 0; i < n; i++) {
            endTimes[i] = eventsByEnd[i][1];
            prefixMax[i] = Math.Max(
                i > 0 ? prefixMax[i - 1] : 0, 
                eventsByEnd[i][2]
            );
        }
        
        // Инициализируем ответ максимальной ценностью одного события
        int maxValue = events.Max(e => e[2]);
        
        // Перебираем все события как вторые
        foreach (var e in events) {
            int start = e[0];
            int value = e[2];
            
            // Бинарный поиск последнего индекса, где endTimes[i] < start
            int idx = BinarySearchLastLessThan(endTimes, start);
            
            if (idx >= 0) {
                maxValue = Math.Max(maxValue, prefixMax[idx] + value);
            }
        }
        
        return maxValue;
    }
    
    /// <summary>
    /// Бинарный поиск последнего индекса, где arr[i] < target
    /// Возвращает -1, если такого элемента нет
    /// </summary>
    private int BinarySearchLastLessThan(int[] arr, int target) {
        int left = 0;
        int right = arr.Length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] < target) {
                result = mid;     // Нашли подходящий индекс, но может быть лучше справа
                left = mid + 1;   // Ищем дальше справа
            } else {
                right = mid - 1;  // Слишком большой, ищем слева
            }
        }
        
        return result;
    }
}