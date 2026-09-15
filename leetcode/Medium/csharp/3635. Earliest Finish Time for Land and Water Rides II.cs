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
    /**
     * Находит минимальное время завершения одного наземного и одного водного аттракциона.
     * 
     * Турист должен посетить ровно один наземный и ровно один водный аттракцион
     * в любом порядке. Аттракцион можно начать в момент его открытия или позже.
     * Если аттракцион начат в момент t, он заканчивается в t + duration.
     * После завершения одного аттракциона можно сразу начать другой или подождать его открытия.
     * 
     * Алгоритм:
     * 1. Рассматриваем оба порядка: land→water и water→land
     * 2. Для каждого аттракциона первого типа находим оптимальный аттракцион второго типа
     * 3. Используем формулу: finish = max(first_end, second_start) + second_duration
     * 4. Сортируем аттракционы второго типа по времени начала
     * 5. Строим префиксные минимумы длительностей и суффиксные минимумы времени завершения
     * 6. Для каждого первого аттракциона бинарным поиском находим границу
     *    и за O(1) получаем оптимальное время
     * 
     * @param landStartTime Времена открытия наземных аттракционов
     * @param landDuration Длительности наземных аттракционов
     * @param waterStartTime Времена открытия водных аттракционов
     * @param waterDuration Длительности водных аттракционов
     * @return Минимальное возможное время завершения обоих аттракционов
     * 
     * Временная сложность: O(N log M + M log M)
     * Пространственная сложность: O(N + M)
     * 
     * Пример:
     * landStartTime = [2, 8], landDuration = [4, 1]
     * waterStartTime = [6], waterDuration = [3]
     * Результат: 9
     */
    public int EarliestFinishTime(int[] landStartTime, int[] landDuration,
                                   int[] waterStartTime, int[] waterDuration) {
        // Вычисляем минимальное время для обоих порядков
        long landFirst = Solve(landStartTime, landDuration, waterStartTime, waterDuration);
        long waterFirst = Solve(waterStartTime, waterDuration, landStartTime, landDuration);
        
        return (int) Math.Min(landFirst, waterFirst);
    }
    
    /**
     * Вычисляет минимальное время для порядка: сначала first, потом second.
     * 
     * Для каждого аттракциона первого типа перебираем все возможные
     * аттракционы второго типа и находим минимальное время завершения.
     * Оптимизация достигается за счёт сортировки и предподсчёта минимумов.
     * 
     * @param firstStart Времена открытия аттракционов первого типа
     * @param firstDur Длительности аттракционов первого типа
     * @param secondStart Времена открытия аттракционов второго типа
     * @param secondDur Длительности аттракционов второго типа
     * @return Минимальное время завершения для данного порядка
     */
    private long Solve(int[] firstStart, int[] firstDur,
                       int[] secondStart, int[] secondDur) {
        int n = firstStart.Length;
        int m = secondStart.Length;
        
        // Создаём массив аттракционов второго типа: (start, duration)
        var second = new (int start, int duration)[m];
        for (int i = 0; i < m; i++) {
            second[i] = (secondStart[i], secondDur[i]);
        }
        
        // Сортируем по времени начала
        Array.Sort(second, (a, b) => a.start.CompareTo(b.start));
        
        // Массив времён начала для бинарного поиска
        int[] starts = new int[m];
        for (int i = 0; i < m; i++) {
            starts[i] = second[i].start;
        }
        
        // Префиксный минимум длительностей
        // prefMinDur[i] = минимальная длительность среди первых i аттракционов
        long[] prefMinDur = new long[m + 1];
        Array.Fill(prefMinDur, long.MaxValue);
        for (int i = 0; i < m; i++) {
            prefMinDur[i + 1] = Math.Min(prefMinDur[i], second[i].duration);
        }
        
        // Суффиксный минимум времён завершения
        // suffMinFinish[i] = минимальное время завершения среди аттракционов с индексом >= i
        long[] suffMinFinish = new long[m + 1];
        Array.Fill(suffMinFinish, long.MaxValue);
        for (int i = m - 1; i >= 0; i--) {
            long finish = (long) second[i].start + second[i].duration;
            suffMinFinish[i] = Math.Min(suffMinFinish[i + 1], finish);
        }
        
        long ans = long.MaxValue;
        
        for (int i = 0; i < n; i++) {
            // Время завершения первого аттракциона
            long firstEnd = (long) firstStart[i] + firstDur[i];
            
            // Бинарный поиск: находим первый second, у которого start >= firstEnd
            int idx = Array.BinarySearch(starts, (int) firstEnd);
            if (idx < 0) {
                idx = ~idx; // Преобразуем в индекс первого элемента >= firstEnd
            }
            
            // Случай 1: second начинается после завершения first
            // finish = second_finish
            if (idx < m) {
                ans = Math.Min(ans, suffMinFinish[idx]);
            }
            
            // Случай 2: second уже открыт к моменту завершения first
            // finish = firstEnd + second_duration
            if (idx > 0) {
                ans = Math.Min(ans, firstEnd + prefMinDur[idx]);
            }
        }
        
        return ans;
    }
}