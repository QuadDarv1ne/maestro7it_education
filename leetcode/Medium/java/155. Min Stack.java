/**
 * https://leetcode.com/problems/min-stack/description/
 */

import java.util.Deque;
import java.util.ArrayDeque;

class MinStack {
    private Deque<Integer> stack;     // основной стек
    private Deque<Integer> minStack;  // стек минимумов

    /**
     * Конструктор: создаёт пустой стек.
     */
    public MinStack() {
        stack = new ArrayDeque<>();
        minStack = new ArrayDeque<>();
    }

    /**
     * Добавляет элемент val в стек.
     * Если стек минимумов пуст или val <= текущего минимума,
     * в стек минимумов помещается val, иначе — текущий минимум.
     */
    public void push(int val) {
        stack.push(val);
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
        } else {
            minStack.push(minStack.peek());
        }
    }

    /**
     * Удаляет верхний элемент из обоих стеков.
     */
    public void pop() {
        stack.pop();
        minStack.pop();
    }

    /**
     * Возвращает верхний элемент основного стека.
     */
    public int top() {
        return stack.peek();
    }

    /**
     * Возвращает текущий минимальный элемент стека.
     */
    public int getMin() {
        return minStack.peek();
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