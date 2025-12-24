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
 * - Время: O(n log n) из-за сортировки и бинарного поиска
 * - Память: O(n) для хранения отсортированных массивов и префиксных максимумов
 */

#include <vector>
#include <algorithm>
#include <functional>

using namespace std;

class Solution {
public:
    int maxTwoEvents(vector<vector<int>>& events) {
        /**
         * Находит максимальную сумму ценностей не более чем двух непересекающихся событий.
         * 
         * Args:
         *   events: vector<vector<int>> - события в формате [начало, конец, ценность]
         * 
         * Returns:
         *   int - максимальная сумма ценностей
         * 
         * Автор: Дуплей Максим Игоревич
         * ORCID: https://orcid.org/0009-0007-7605-539X
         * GitHub: https://github.com/QuadDarv1ne/
         */
        
        int n = events.size();
        
        // Сортируем события по времени окончания
        vector<vector<int>> events_by_end = events;
        sort(events_by_end.begin(), events_by_end.end(), 
             [](const vector<int>& a, const vector<int>& b) {
                 return a[1] < b[1];
             });
        
        // Создаем массивы времен окончания и префиксных максимумов
        vector<int> end_times(n);
        vector<int> prefix_max(n);
        
        for (int i = 0; i < n; i++) {
            end_times[i] = events_by_end[i][1];
            if (i == 0) {
                prefix_max[i] = events_by_end[i][2];
            } else {
                prefix_max[i] = max(prefix_max[i-1], events_by_end[i][2]);
            }
        }
        
        // Находим максимальную ценность одного события
        int max_value = 0;
        for (const auto& event : events) {
            max_value = max(max_value, event[2]);
        }
        
        // Перебираем каждое событие как второе
        for (const auto& event : events) {
            int start = event[0];
            int value = event[2];
            
            // Бинарный поиск последнего события, которое заканчивается до start
            auto it = lower_bound(end_times.begin(), end_times.end(), start);
            int idx = distance(end_times.begin(), it) - 1;
            
            if (idx >= 0) {
                max_value = max(max_value, prefix_max[idx] + value);
            }
        }
        
        return max_value;
    }
};