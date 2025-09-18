/**
 * https://leetcode.com/problems/design-task-manager/description/?envType=daily-question&envId=2025-09-18
 */

import java.util.*;

/**
 * Менеджер задач.
 *
 * Описание:
 *  - Конструктор принимает массив задач int[][] tasks, каждая запись:
 *    [userId, taskId, priority].
 *  - add(userId, taskId, priority) — добавить задачу.
 *  - edit(taskId, newPriority) — изменить приоритет.
 *  - rmv(taskId) — удалить задачу.
 *  - execTop() — выполнить и удалить задачу с наивысшим приоритетом и вернуть userId.
 *
 * Порядок выбора:
 *  - Сначала по большему priority;
 *  - при равных priority — по большему taskId.
 *
 * Реализация:
 *  - PriorityQueue + Map для ленивой проверки актуальности записей.
 */
public class TaskManager {
    private PriorityQueue<int[]> pq;
    private Map<Integer, int[]> active; // taskId -> {priority, userId}

    /**
     * Конструктор.
     * @param tasks массив задач (каждая запись: [userId, taskId, priority])
     */
    public TaskManager(int[][] tasks) {
        pq = new PriorityQueue<>((a,b) -> {
            if (a[0] != b[0]) return Integer.compare(b[0], a[0]); // больший priority раньше
            if (a[1] != b[1]) return Integer.compare(b[1], a[1]); // больший taskId раньше
            return Integer.compare(a[2], b[2]); // финальный tie-break
        });
        active = new HashMap<>();
        if (tasks != null) {
            for (int[] t : tasks) {
                // t = [userId, taskId, priority]
                add(t[0], t[1], t[2]);
            }
        }
    }

    /** Добавить задачу. */
    public void add(int userId, int taskId, int priority) {
        active.put(taskId, new int[]{priority, userId});
        pq.offer(new int[]{priority, taskId, userId});
    }

    /** Изменить приоритет задачи. */
    public void edit(int taskId, int newPriority) {
        int[] cur = active.get(taskId);
        if (cur != null) {
            int userId = cur[1];
            active.put(taskId, new int[]{newPriority, userId});
            pq.offer(new int[]{newPriority, taskId, userId});
        }
    }

    /** Удалить задачу. */
    public void rmv(int taskId) {
        active.remove(taskId);
    }

    /**
     * Выполнить и удалить задачу с наивысшим приоритетом.
     * @return userId выполненной задачи или -1
     */
    public int execTop() {
        while (!pq.isEmpty()) {
            int[] top = pq.poll();
            int pr = top[0], tid = top[1], uid = top[2];
            int[] cur = active.get(tid);
            if (cur != null && cur[0] == pr && cur[1] == uid) {
                active.remove(tid);
                return uid;
            }
            // иначе устаревшая запись — пропускаем
        }
        return -1;
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/