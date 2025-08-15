/**
 * https://leetcode.com/problems/min-stack/description/
 */

/**
 * Реализация MinStack с поддержкой получения минимума за O(1).
 * 
 * Конструктор:
 * - this.stack — основной стек.
 * - this.minStack — стек минимумов.
 */
class MinStack {
    constructor() {
        this.stack = [];
        this.minStack = [];
    }

    /**
     * Добавляет элемент val в стек.
     * Если стек минимумов пуст или val <= текущего минимума,
     * в стек минимумов помещается val, иначе — текущий минимум.
     */
    push(val) {
        this.stack.push(val);
        if (this.minStack.length === 0 || val <= this.minStack[this.minStack.length - 1]) {
            this.minStack.push(val);
        } else {
            this.minStack.push(this.minStack[this.minStack.length - 1]);
        }
    }

    /**
     * Удаляет верхний элемент из обоих стеков.
     */
    pop() {
        this.stack.pop();
        this.minStack.pop();
    }

    /**
     * Возвращает верхний элемент основного стека.
     */
    top() {
        return this.stack[this.stack.length - 1];
    }

    /**
     * Возвращает текущий минимальный элемент стека.
     */
    getMin() {
        return this.minStack[this.minStack.length - 1];
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/