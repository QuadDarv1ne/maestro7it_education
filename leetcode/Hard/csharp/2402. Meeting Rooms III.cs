using System;
using System.Collections.Generic;
using System.Linq;

public class Solution {
    /**
     * Находит номер комнаты, в которой прошло больше всего встреч.
     * 
     * @param n количество комнат (0..n-1)
     * @param meetings список встреч [начало, конец]
     * @return Номер комнаты с максимальным количеством встреч (наименьший при равенстве)
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
    public int MostBooked(int n, int[][] meetings) {
        // Сортируем встречи по времени начала
        Array.Sort(meetings, (a, b) => a[0].CompareTo(b[0]));
        
        // Мини-куча для свободных комнат
        var freeRooms = new PriorityQueue<int, int>();
        for (int i = 0; i < n; i++) {
            freeRooms.Enqueue(i, i);
        }
        
        // Мини-куча для занятых комнат: приоритет по времени окончания
        // Используем long для избежания переполнения
        var busyRooms = new PriorityQueue<(int room, long endTime), (long endTime, int room)>();
        
        // Счетчик встреч для каждой комнаты
        int[] roomCount = new int[n];
        
        foreach (var meeting in meetings) {
            long start = meeting[0];
            long end = meeting[1];
            long duration = end - start;
            
            // Освобождаем комнаты, встречи в которых закончились
            while (busyRooms.Count > 0 && busyRooms.Peek().endTime <= start) {
                var (room, _) = busyRooms.Dequeue();
                freeRooms.Enqueue(room, room);
            }
            
            // Текущее время для начала встречи
            long currentTime = start;
            
            if (freeRooms.Count > 0) {
                // Есть свободная комната - берем с наименьшим номером
                int room = freeRooms.Dequeue();
                roomCount[room]++;
                // Встреча начинается сразу
                busyRooms.Enqueue((room, currentTime + duration), (currentTime + duration, room));
            } else {
                // Нет свободных комнат - ждем освобождения первой
                var (room, endTime) = busyRooms.Dequeue();
                
                // Встреча задерживается до освобождения комнаты
                currentTime = Math.Max(currentTime, endTime);
                roomCount[room]++;
                
                // Новая встреча начинается после окончания предыдущей
                busyRooms.Enqueue((room, currentTime + duration), (currentTime + duration, room));
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
}