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

#include <vector>
#include <queue>
#include <set>
#include <algorithm>

using namespace std;

class Solution {
public:
    vector<vector<int>> getSkyline(vector<vector<int>>& buildings) {
        vector<vector<int>> result;
        if (buildings.empty()) return result;
        
        // Создаем события: для каждого здания - начало (отрицательная высота) и конец (положительная высота)
        vector<pair<int, int>> events;
        for (const auto& building : buildings) {
            events.push_back({building[0], -building[2]});  // Начало здания
            events.push_back({building[1], building[2]});   // Конец здания
        }
        
        // Сортируем события по координате X
        // При одинаковом X: начала обрабатываем до концов, более высокие здания раньше
        sort(events.begin(), events.end());
        
        // Мультимножество для хранения текущих высот (автоматически сортируется)
        multiset<int> heights = {0};
        
        // Предыдущая максимальная высота
        int prevMax = 0;
        
        // Обрабатываем события
        for (const auto& event : events) {
            int x = event.first;
            int height = event.second;
            
            if (height < 0) {
                // Начало здания - добавляем высоту
                heights.insert(-height);
            } else {
                // Конец здания - удаляем высоту
                heights.erase(heights.find(height));
            }
            
            // Текущая максимальная высота
            int currentMax = *heights.rbegin();
            
            // Если высота изменилась - добавляем точку
            if (currentMax != prevMax) {
                result.push_back({x, currentMax});
                prevMax = currentMax;
            }
        }
        
        return result;
    }
};