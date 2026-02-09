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

/**
 * Реализация стека с использованием двух очередей.
 * Используется подход с дорогой операцией push.
 * 
 * Сложность операций:
 * - push: O(n)
 * - pop: O(1)
 * - top: O(1)
 * - empty: O(1)
 */
var MyStack = function() {
    /**
     * Инициализирует стек с двумя пустыми массивами, используемыми как очереди.
     */
    this.mainQueue = [];
    this.tempQueue = [];
};

/**
 * Помещает элемент x на вершину стека.
 * 
 * Алгоритм:
 * 1. Добавить x во временную очередь
 * 2. Переместить все элементы из основной очереди во временную
 * 3. Поменять очереди местами
 * 
 * @param {number} x Элемент для добавления в стек
 * @return {void}
 */
MyStack.prototype.push = function(x) {
    // Добавляем новый элемент во временную очередь
    this.tempQueue.push(x);
    
    // Перемещаем все элементы из основной очереди во временную
    while (this.mainQueue.length > 0) {
        this.tempQueue.push(this.mainQueue.shift());
    }
    
    // Меняем очереди местами
    [this.mainQueue, this.tempQueue] = [this.tempQueue, this.mainQueue];
};

/**
 * Удаляет элемент с вершины стека и возвращает его.
 * 
 * @return {number} Элемент с вершины стека
 * @throws {Error} Если стек пуст
 */
MyStack.prototype.pop = function() {
    if (this.empty()) {
        throw new Error("Stack is empty");
    }
    return this.mainQueue.shift();
};

/**
 * Возвращает элемент на вершине стека без удаления.
 * 
 * @return {number} Элемент на вершине стека
 * @throws {Error} Если стек пуст
 */
MyStack.prototype.top = function() {
    if (this.empty()) {
        throw new Error("Stack is empty");
    }
    return this.mainQueue[0];
};

/**
 * Проверяет, пуст ли стек.
 * 
 * @return {boolean} true, если стек пуст, иначе false
 */
MyStack.prototype.empty = function() {
    return this.mainQueue.length === 0;
};

/**
 * Пример использования:
 * 
 * var obj = new MyStack()
 * obj.push(1)
 * obj.push(2)
 * var param_2 = obj.pop()    // 2
 * var param_3 = obj.top()    // 1
 * var param_4 = obj.empty()  // false
 */

// Альтернативная реализация с использованием одного массива (простой подход)
class MyStackSimple {
    constructor() {
        this.queue = [];
    }
    
    push(x) {
        // Добавляем элемент в конец
        this.queue.push(x);
        // Перемещаем все предыдущие элементы после нового
        for (let i = 0; i < this.queue.length - 1; i++) {
            this.queue.push(this.queue.shift());
        }
    }
    
    pop() {
        return this.queue.shift();
    }
    
    top() {
        return this.queue[0];
    }
    
    empty() {
        return this.queue.length === 0;
    }
}