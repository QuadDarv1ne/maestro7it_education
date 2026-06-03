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

#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

class Solution {
public:
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
    int earliestFinishTime(vector<int>& landStartTime, vector<int>& landDuration,
                           vector<int>& waterStartTime, vector<int>& waterDuration) {
        // Вспомогательная функция для вычисления минимального времени
        // при порядке: сначала first, потом second
        auto solve = [](vector<int>& first_start, vector<int>& first_dur,
                        vector<int>& second_start, vector<int>& second_dur) -> long long {
            int n = first_start.size();
            int m = second_start.size();
            
            // Создаём массив аттракционов второго типа: {start, duration}
            vector<pair<int, int>> second(m);
            for (int i = 0; i < m; i++) {
                second[i] = {second_start[i], second_dur[i]};
            }
            
            // Сортируем по времени начала
            sort(second.begin(), second.end());
            
            // Массив времён начала для бинарного поиска
            vector<int> starts(m);
            for (int i = 0; i < m; i++) {
                starts[i] = second[i].first;
            }
            
            // Префиксный минимум длительностей
            // pref_min_dur[i] = минимальная длительность среди первых i аттракционов
            vector<long long> pref_min_dur(m + 1, LLONG_MAX);
            for (int i = 0; i < m; i++) {
                pref_min_dur[i + 1] = min(pref_min_dur[i], (long long)second[i].second);
            }
            
            // Суффиксный минимум времён завершения
            // suff_min_finish[i] = минимальное время завершения среди аттракционов с индексом >= i
            vector<long long> suff_min_finish(m + 1, LLONG_MAX);
            for (int i = m - 1; i >= 0; i--) {
                long long finish = (long long)second[i].first + second[i].second;
                suff_min_finish[i] = min(suff_min_finish[i + 1], finish);
            }
            
            long long ans = LLONG_MAX;
            
            for (int i = 0; i < n; i++) {
                // Время завершения первого аттракциона
                long long first_end = (long long)first_start[i] + first_dur[i];
                
                // Бинарный поиск: находим первый second, у которого start >= first_end
                int idx = lower_bound(starts.begin(), starts.end(), (int)first_end) - starts.begin();
                
                // Случай 1: second начинается после завершения first
                // finish = second_finish
                if (idx < m) {
                    ans = min(ans, suff_min_finish[idx]);
                }
                
                // Случай 2: second уже открыт к моменту завершения first
                // finish = first_end + second_duration
                if (idx > 0) {
                    ans = min(ans, first_end + pref_min_dur[idx]);
                }
            }
            
            return ans;
        };
        
        // Вычисляем минимальное время для обоих порядков
        long long land_first = solve(landStartTime, landDuration, waterStartTime, waterDuration);
        long long water_first = solve(waterStartTime, waterDuration, landStartTime, landDuration);
        
        return (int)min(land_first, water_first);
    }
};