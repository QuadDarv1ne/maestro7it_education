/**
 * https://leetcode.com/problems/design-task-manager/description/?envType=daily-question&envId=2025-09-18
 */

/**
 * Менеджер задач (JS).
 *
 * Описание:
 *  - Конструктор принимает tasks: массив записей [userId, taskId, priority].
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
 *  - Собственная реализация max-heap + Map для ленивой проверки актуальности.
 */

class TaskManager {
    constructor(tasks) {
        // heap хранит объекты {pr, tid, uid}
        this.heap = [];
        this.active = new Map(); // taskId -> [priority, userId]
        if (tasks) {
            for (const t of tasks) {
                // t = [userId, taskId, priority]
                this.add(t[0], t[1], t[2]);
            }
        }
    }

    // сравнение: возвращает true если a выше b (в max-heap)
    cmp(a, b) {
        if (a.pr !== b.pr) return a.pr > b.pr;    // больший priority выше
        if (a.tid !== b.tid) return a.tid > b.tid; // больший taskId выше
        return a.uid > b.uid;
    }

    swap(i, j) {
        const t = this.heap[i]; this.heap[i] = this.heap[j]; this.heap[j] = t;
    }

    push(node) {
        this.heap.push(node);
        let i = this.heap.length - 1;
        while (i > 0) {
            const p = Math.floor((i - 1) / 2);
            if (this.cmp(this.heap[i], this.heap[p])) {
                this.swap(i, p);
                i = p;
            } else break;
        }
    }

    pop() {
        if (this.heap.length === 0) return null;
        const top = this.heap[0];
        const end = this.heap.pop();
        if (this.heap.length > 0) {
            this.heap[0] = end;
            this.heapify(0);
        }
        return top;
    }

    heapify(i) {
        const n = this.heap.length;
        while (true) {
            let best = i;
            const l = 2*i + 1, r = 2*i + 2;
            if (l < n && this.cmp(this.heap[l], this.heap[best])) best = l;
            if (r < n && this.cmp(this.heap[r], this.heap[best])) best = r;
            if (best === i) break;
            this.swap(i, best);
            i = best;
        }
    }

    /** Добавить задачу. */
    add(userId, taskId, priority) {
        this.active.set(taskId, [priority, userId]);
        this.push({pr: priority, tid: taskId, uid: userId});
    }

    /** Изменить приоритет задачи, если она существует. */
    edit(taskId, newPriority) {
        const cur = this.active.get(taskId);
        if (cur !== undefined) {
            const userId = cur[1];
            this.active.set(taskId, [newPriority, userId]);
            this.push({pr: newPriority, tid: taskId, uid: userId});
        }
    }

    /** Удалить задачу (ленивое удаление). */
    rmv(taskId) {
        this.active.delete(taskId);
    }

    /**
     * Выполнить и удалить задачу с наивысшим приоритетом.
     * Возвращает userId выполненной задачи или -1.
     */
    execTop() {
        while (this.heap.length > 0) {
            const node = this.pop();
            const cur = this.active.get(node.tid);
            if (cur !== undefined && cur[0] === node.pr && cur[1] === node.uid) {
                this.active.delete(node.tid);
                return node.uid;
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