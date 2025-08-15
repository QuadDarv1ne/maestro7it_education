/**
 * https://leetcode.com/problems/min-stack/description/
 */

using System.Collections.Generic;

public class MinStack {
    private Stack<int> stack;     // основной стек
    private Stack<int> minStack;  // стек минимумов

    /// <summary>
    /// Конструктор: создаёт пустой MinStack.
    /// </summary>
    public MinStack() {
        stack = new Stack<int>();
        minStack = new Stack<int>();
    }

    /// <summary>
    /// Добавляет элемент val в стек.
    /// Если стек минимумов пуст или val <= текущего минимума,
    /// в стек минимумов помещается val, иначе — текущий минимум.
    /// </summary>
    public void Push(int val) {
        stack.Push(val);
        if (minStack.Count == 0 || val <= minStack.Peek())
            minStack.Push(val);
        else
            minStack.Push(minStack.Peek());
    }

    /// <summary>
    /// Удаляет верхний элемент из обоих стеков.
    /// </summary>
    public void Pop() {
        stack.Pop();
        minStack.Pop();
    }

    /// <summary>
    /// Возвращает верхний элемент основного стека.
    /// </summary>
    public int Top() {
        return stack.Peek();
    }

    /// <summary>
    /// Возвращает текущий минимальный элемент стека.
    /// </summary>
    public int GetMin() {
        return minStack.Peek();
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