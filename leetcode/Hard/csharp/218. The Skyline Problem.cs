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

using System;
using System.Collections.Generic;

public class Solution {
    public IList<IList<int>> GetSkyline(int[][] buildings) {
        List<IList<int>> result = new List<IList<int>>();
        if (buildings == null || buildings.Length == 0) return result;
        
        // Создаем список всех точек событий
        List<int[]> events = new List<int[]>();
        
        foreach (var building in buildings) {
            int left = building[0];
            int right = building[1];
            int height = building[2];
            
            // Начало здания - отрицательная высота
            events.Add(new int[] { left, -height });
            // Конец здания - положительная высота
            events.Add(new int[] { right, height });
        }
        
        // Сортируем события
        events.Sort((a, b) => {
            if (a[0] != b[0]) return a[0].CompareTo(b[0]);
            // При одинаковом X: начала перед концами
            return a[1].CompareTo(b[1]);
        });
        
        // Максимальная куча для хранения текущих высот
        // Используем SortedDictionary для эмуляции max-heap
        SortedDictionary<int, int> heightCounts = new SortedDictionary<int, int>();
        heightCounts[0] = 1;  // Изначально только уровень земли
        
        // Предыдущая максимальная высота
        int prevMax = 0;
        
        // Обрабатываем события
        foreach (var ev in events) {
            int x = ev[0];
            int height = ev[1];
            
            if (height < 0) {
                // Начало здания
                height = -height;
                if (heightCounts.ContainsKey(height)) {
                    heightCounts[height]++;
                } else {
                    heightCounts[height] = 1;
                }
            } else {
                // Конец здания
                if (heightCounts[height] == 1) {
                    heightCounts.Remove(height);
                } else {
                    heightCounts[height]--;
                }
            }
            
            // Текущая максимальная высота
            int currentMax = GetMaxHeight(heightCounts);
            
            // Если высота изменилась
            if (currentMax != prevMax) {
                result.Add(new List<int> { x, currentMax });
                prevMax = currentMax;
            }
        }
        
        return result;
    }
    
    private int GetMaxHeight(SortedDictionary<int, int> dict) {
        // В SortedDictionary ключи отсортированы по возрастанию
        // Берем последний ключ - максимальную высоту
        int max = 0;
        foreach (var key in dict.Keys) {
            max = key;
        }
        return max;
    }
}