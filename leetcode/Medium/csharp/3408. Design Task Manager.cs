/**
 * https://leetcode.com/problems/design-task-manager/description/?envType=daily-question&envId=2025-09-18
 */

using System;
using System.Collections.Generic;

/// <summary>
/// Менеджер задач.
/// 
/// Поведение:
///  - Конструктор принимает массив задач int[][] tasks, где каждая запись
///    имеет формат [userId, taskId, priority].
///  - Add(userId, taskId, priority) — добавить задачу.
///  - Edit(taskId, newPriority) — изменить приоритет задачи.
///  - Rmv(taskId) — удалить задачу.
///  - ExecTop() — выполнить и удалить задачу с наивысшим приоритетом и
///    вернуть userId; если задач нет — вернуть -1.
/// 
/// Правила выбора:
///  - Сначала по большему priority;
///  - при равных priority — по большему taskId.
/// 
/// Реализация:
///  - Собственная реализация binary heap (max-heap);
///  - Словарь active для ленивой проверки актуальности записей.
/// </summary>
public class TaskManager {
    class Node {
        public int pr;
        public int tid;
        public int uid;
        public Node(int _pr,int _tid,int _uid){ pr=_pr; tid=_tid; uid=_uid; }
    }

    List<Node> heap = new List<Node>();
    Dictionary<int, (int priority, int userId)> active = new Dictionary<int, (int,int)>();

    /// <summary>
    /// Конструктор: принимает массив задач (каждая запись: [userId, taskId, priority]).
    /// </summary>
    public TaskManager(int[][] tasks) {
        if (tasks != null) {
            foreach (var t in tasks) {
                // t: [userId, taskId, priority]
                Add(t[0], t[1], t[2]);
            }
        }
    }

    // сравнение: больший priority выше, при равенстве больший taskId выше
    private bool Higher(Node a, Node b) {
        if (a.pr != b.pr) return a.pr > b.pr;
        if (a.tid != b.tid) return a.tid > b.tid;
        return a.uid > b.uid;
    }

    private void Swap(int i, int j) {
        var tmp = heap[i]; heap[i] = heap[j]; heap[j] = tmp;
    }

    private void SiftUp(int i) {
        while (i > 0) {
            int p = (i - 1) / 2;
            if (Higher(heap[i], heap[p])) { Swap(i, p); i = p; }
            else break;
        }
    }

    private void SiftDown(int i) {
        int n = heap.Count;
        while (true) {
            int l = 2*i + 1, r = 2*i + 2, best = i;
            if (l < n && Higher(heap[l], heap[best])) best = l;
            if (r < n && Higher(heap[r], heap[best])) best = r;
            if (best == i) break;
            Swap(i, best);
            i = best;
        }
    }

    /// <summary>
    /// Добавить задачу.
    /// </summary>
    public void Add(int userId, int taskId, int priority) {
        active[taskId] = (priority, userId);
        var node = new Node(priority, taskId, userId);
        heap.Add(node);
        SiftUp(heap.Count - 1);
    }

    /// <summary>
    /// Изменить приоритет задачи, если она существует.
    /// </summary>
    public void Edit(int taskId, int newPriority) {
        if (active.ContainsKey(taskId)) {
            var pair = active[taskId];
            int userId = pair.userId;
            active[taskId] = (newPriority, userId);
            var node = new Node(newPriority, taskId, userId);
            heap.Add(node);
            SiftUp(heap.Count - 1);
        }
    }

    /// <summary>
    /// Удалить задачу (из active — ленивое удаление).
    /// </summary>
    public void Rmv(int taskId) {
        active.Remove(taskId);
    }

    /// <summary>
    /// Выполнить и удалить задачу с наивысшим приоритетом; вернуть userId или -1.
    /// </summary>
    public int ExecTop() {
        while (heap.Count > 0) {
            var top = heap[0];
            // извлечём вершину
            heap[0] = heap[heap.Count - 1];
            heap.RemoveAt(heap.Count - 1);
            if (heap.Count > 0) SiftDown(0);

            if (active.TryGetValue(top.tid, out var cur)) {
                if (cur.priority == top.pr && cur.userId == top.uid) {
                    active.Remove(top.tid);
                    return top.uid;
                }
            }
            // иначе устаревшая запись — пропускаем и продолжаем
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