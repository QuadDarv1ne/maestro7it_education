#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

class Solution {
public:
    int mostBooked(int n, vector<vector<int>>& meetings) {
        /**
         * Находит номер комнаты, в которой прошло больше всего встреч.
         * 
         * Args:
         *   n: количество комнат (0..n-1)
         *   meetings: список встреч [начало, конец]
         * 
         * Returns:
         *   Номер комнаты с максимальным количеством встреч (наименьший при равенстве)
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
         */
        
        // Сортируем встречи по времени начала
        sort(meetings.begin(), meetings.end());
        
        // Мини-куча для свободных комнат (храним номера)
        priority_queue<int, vector<int>, greater<int>> freeRooms;
        for (int i = 0; i < n; i++) {
            freeRooms.push(i);
        }
        
        // Мини-куча для занятых комнат: (время окончания, номер комнаты)
        // Используем long long для избежания переполнения
        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> busyRooms;
        
        // Счетчик встреч для каждой комнаты
        vector<int> roomCount(n, 0);
        
        for (auto& meeting : meetings) {
            long long start = meeting[0];
            long long end = meeting[1];
            long long duration = end - start;
            
            // Освобождаем комнаты, встречи в которых закончились
            while (!busyRooms.empty() && busyRooms.top().first <= start) {
                int room = busyRooms.top().second;
                busyRooms.pop();
                freeRooms.push(room);
            }
            
            // Текущее время для начала встречи
            long long currentTime = start;
            
            if (!freeRooms.empty()) {
                // Есть свободная комната - берем с наименьшим номером
                int room = freeRooms.top();
                freeRooms.pop();
                roomCount[room]++;
                // Встреча начинается сразу
                busyRooms.push({currentTime + duration, room});
            } else {
                // Нет свободных комнат - ждем освобождения первой
                auto [endTime, room] = busyRooms.top();
                busyRooms.pop();
                
                // Встреча задерживается до освобождения комнаты
                currentTime = max(currentTime, endTime);
                roomCount[room]++;
                
                // Новая встреча начинается после окончания предыдущей
                busyRooms.push({currentTime + duration, room});
            }
        }
        
        // Находим комнату с максимальным количеством встреч
        int maxRoom = 0;
        for (int i = 1; i < n; i++) {
            if (roomCount[i] > roomCount[maxRoom]) {
                maxRoom = i;
            }
        }
        
        return maxRoom;
    }
};