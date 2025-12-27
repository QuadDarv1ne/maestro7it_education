/**
 * Находит номер комнаты, в которой прошло больше всего встреч.
 * 
 * @param {number} n - количество комнат (0..n-1)
 * @param {number[][]} meetings - список встреч [начало, конец]
 * @return {number} - номер комнаты с максимальным количеством встреч (наименьший при равенстве)
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
var mostBooked = function(n, meetings) {
    // Вложенный класс MinHeap для избежания конфликта имен
    class MinHeap {
        constructor(comparator = (a, b) => a - b) {
            this.heap = [];
            this.comparator = comparator;
        }
        
        push(value) {
            this.heap.push(value);
            this.bubbleUp(this.heap.length - 1);
        }
        
        pop() {
            if (this.isEmpty()) return null;
            const root = this.heap[0];
            const last = this.heap.pop();
            if (this.heap.length > 0) {
                this.heap[0] = last;
                this.bubbleDown(0);
            }
            return root;
        }
        
        peek() {
            return this.heap[0] || null;
        }
        
        isEmpty() {
            return this.heap.length === 0;
        }
        
        bubbleUp(index) {
            while (index > 0) {
                const parent = Math.floor((index - 1) / 2);
                if (this.comparator(this.heap[index], this.heap[parent]) >= 0) break;
                [this.heap[index], this.heap[parent]] = [this.heap[parent], this.heap[index]];
                index = parent;
            }
        }
        
        bubbleDown(index) {
            const last = this.heap.length - 1;
            while (true) {
                let smallest = index;
                const left = index * 2 + 1;
                const right = index * 2 + 2;
                
                if (left <= last && this.comparator(this.heap[left], this.heap[smallest]) < 0) {
                    smallest = left;
                }
                if (right <= last && this.comparator(this.heap[right], this.heap[smallest]) < 0) {
                    smallest = right;
                }
                if (smallest === index) break;
                
                [this.heap[index], this.heap[smallest]] = [this.heap[smallest], this.heap[index]];
                index = smallest;
            }
        }
    }

    // Сортируем встречи по времени начала
    meetings.sort((a, b) => a[0] - b[0]);
    
    // Мини-куча для свободных комнат
    const freeRooms = new MinHeap();
    for (let i = 0; i < n; i++) {
        freeRooms.push(i);
    }
    
    // Мини-куча для занятых комнат: (время окончания, номер комнаты)
    // Используем BigInt для избежания переполнения
    const busyRooms = new MinHeap((a, b) => {
        if (a[0] === b[0]) {
            return a[1] - b[1];
        }
        return Number(a[0] - b[0]);
    });
    
    // Счетчик встреч для каждой комнаты
    const roomCount = new Array(n).fill(0);
    
    for (const [start, end] of meetings) {
        const duration = BigInt(end - start);
        const startBig = BigInt(start);
        
        // Освобождаем комнаты, встречи в которых закончились
        while (!busyRooms.isEmpty() && busyRooms.peek()[0] <= startBig) {
            const [, room] = busyRooms.pop();
            freeRooms.push(room);
        }
        
        // Текущее время для начала встречи
        let currentTime = startBig;
        
        if (!freeRooms.isEmpty()) {
            // Есть свободная комната - берем с наименьшим номером
            const room = freeRooms.pop();
            roomCount[room]++;
            // Встреча начинается сразу
            busyRooms.push([currentTime + duration, room]);
        } else {
            // Нет свободных комнат - ждем освобождения первой
            const [endTime, room] = busyRooms.pop();
            
            // Встреча задерживается до освобождения комнаты
            currentTime = currentTime > endTime ? currentTime : endTime;
            roomCount[room]++;
            
            // Новая встреча начинается после окончания предыдущей
            busyRooms.push([currentTime + duration, room]);
        }
    }
    
    // Находим комнату с максимальным количеством встреч
    let maxRoom = 0;
    for (let i = 1; i < n; i++) {
        if (roomCount[i] > roomCount[maxRoom]) {
            maxRoom = i;
        }
    }
    
    return maxRoom;
};