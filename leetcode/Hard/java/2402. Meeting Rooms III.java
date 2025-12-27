import java.util.*;

class Solution {
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
    public int mostBooked(int n, int[][] meetings) {
        // Сортируем встречи по времени начала
        Arrays.sort(meetings, (a, b) -> Integer.compare(a[0], b[0]));
        
        // Мини-куча для свободных комнат
        PriorityQueue<Integer> freeRooms = new PriorityQueue<>();
        for (int i = 0; i < n; i++) {
            freeRooms.offer(i);
        }
        
        // Мини-куча для занятых комнат: (время окончания, номер комнаты)
        // Используем long для избежания переполнения
        PriorityQueue<long[]> busyRooms = new PriorityQueue<>(
            (a, b) -> {
                if (a[0] == b[0]) {
                    return Long.compare(a[1], b[1]);
                }
                return Long.compare(a[0], b[0]);
            }
        );
        
        // Счетчик встреч для каждой комнаты
        int[] roomCount = new int[n];
        
        for (int[] meeting : meetings) {
            long start = meeting[0];
            long end = meeting[1];
            long duration = end - start;
            
            // Освобождаем комнаты, встречи в которых закончились
            while (!busyRooms.isEmpty() && busyRooms.peek()[0] <= start) {
                int room = (int) busyRooms.poll()[1];
                freeRooms.offer(room);
            }
            
            // Текущее время для начала встречи
            long currentTime = start;
            
            if (!freeRooms.isEmpty()) {
                // Есть свободная комната - берем с наименьшим номером
                int room = freeRooms.poll();
                roomCount[room]++;
                // Встреча начинается сразу
                busyRooms.offer(new long[]{currentTime + duration, room});
            } else {
                // Нет свободных комнат - ждем освобождения первой
                long[] busy = busyRooms.poll();
                long endTime = busy[0];
                int room = (int) busy[1];
                
                // Встреча задерживается до освобождения комнаты
                currentTime = Math.max(currentTime, endTime);
                roomCount[room]++;
                
                // Новая встреча начинается после окончания предыдущей
                busyRooms.offer(new long[]{currentTime + duration, room});
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