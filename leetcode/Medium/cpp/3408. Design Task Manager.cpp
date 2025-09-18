/**
 * https://leetcode.com/problems/design-task-manager/description/?envType=daily-question&envId=2025-09-18
 */

#include <bits/stdc++.h>
using namespace std;

struct Node {
    int pr;
    int tid;
    int uid;
};

/**
 * Класс TaskManager реализует менеджер задач.
 *
 * Поведение:
 *  - При инициализации принимает список задач tasks, где каждая запись
 *    имеет формат [userId, taskId, priority].
 *  - add(userId, taskId, priority) — добавить задачу.
 *  - edit(taskId, newPriority) — изменить приоритет существующей задачи.
 *  - rmv(taskId) — удалить задачу (если есть).
 *  - execTop() — выполнить и удалить задачу с наивысшим приоритетом и
 *    вернуть userId этой задачи. При равных priority выбирается большая
 *    taskId. Если задач нет — вернуть -1.
 *
 * Реализация:
 *  - priority_queue (куча) для быстрого доступа к кандидату;
 *  - unordered_map active для ленивой валидации (lazy deletion) устаревших записей.
 */
struct Cmp {
    // вернуть true, если a "меньше" b (чтобы priority_queue давал сверху наибольшее)
    bool operator()(const Node &a, const Node &b) const {
        if (a.pr != b.pr) return a.pr < b.pr;     // больший priority выше
        if (a.tid != b.tid) return a.tid < b.tid; // при равном priority больший taskId выше
        return a.uid < b.uid;                     // финальный tie-break (необязателен)
    }
};

class TaskManager {
    priority_queue<Node, vector<Node>, Cmp> pq;
    unordered_map<int, pair<int,int>> active; // taskId -> (priority, userId)
public:
    /**
     * Конструктор.
     * @param tasks вектор задач, каждая запись: [userId, taskId, priority]
     */
    TaskManager(vector<vector<int>>& tasks) {
        for (auto &t : tasks) {
            // t: [userId, taskId, priority]
            add(t[0], t[1], t[2]);
        }
    }

    /**
     * Добавить задачу.
     */
    void add(int userId, int taskId, int priority) {
        active[taskId] = {priority, userId};
        pq.push(Node{priority, taskId, userId});
    }

    /**
     * Изменить приоритет задачи, если она существует.
     */
    void edit(int taskId, int newPriority) {
        auto it = active.find(taskId);
        if (it != active.end()) {
            int userId = it->second.second;
            it->second.first = newPriority;
            pq.push(Node{newPriority, taskId, userId});
        }
    }

    /**
     * Удалить задачу (ленивое удаление: удаляем только из active).
     */
    void rmv(int taskId) {
        active.erase(taskId);
    }

    /**
     * Выполнить и удалить задачу с наивысшим приоритетом.
     * Возвращает userId выполненной задачи или -1, если задач нет.
     */
    int execTop() {
        while (!pq.empty()) {
            Node top = pq.top(); pq.pop();
            auto it = active.find(top.tid);
            if (it != active.end()) {
                int curPr = it->second.first;
                int curUid = it->second.second;
                if (curPr == top.pr && curUid == top.uid) {
                    active.erase(it);
                    return top.uid;
                }
            }
            // иначе устаревшая запись — пропускаем
        }
        return -1;
    }
};

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