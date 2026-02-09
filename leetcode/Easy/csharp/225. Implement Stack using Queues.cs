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

using System.Collections.Generic;

public class MyStack {
    private Queue<int> mainQueue;
    private Queue<int> tempQueue;
    
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
    public MyStack() {
        mainQueue = new Queue<int>();
        tempQueue = new Queue<int>();
    }
    
    /**
     * Помещает элемент x на вершину стека.
     * 
     * Алгоритм:
     * 1. Добавить x во временную очередь
     * 2. Переместить все элементы из основной очереди во временную
     * 3. Поменять очереди местами
     * 
     * @param x Элемент для добавления в стек
     */
    public void Push(int x) {
        // Добавляем новый элемент во временную очередь
        tempQueue.Enqueue(x);
        
        // Перемещаем все элементы из основной очереди во временную
        while (mainQueue.Count > 0) {
            tempQueue.Enqueue(mainQueue.Dequeue());
        }
        
        // Меняем очереди местами
        var temp = mainQueue;
        mainQueue = tempQueue;
        tempQueue = temp;
    }
    
    /**
     * Удаляет элемент с вершины стека и возвращает его.
     * 
     * @return Элемент с вершины стека
     * @throws InvalidOperationException Если стек пуст
     */
    public int Pop() {
        if (Empty()) {
            throw new System.InvalidOperationException("Stack is empty");
        }
        return mainQueue.Dequeue();
    }
    
    /**
     * Возвращает элемент на вершине стека без удаления.
     * 
     * @return Элемент на вершине стека
     * @throws InvalidOperationException Если стек пуст
     */
    public int Top() {
        if (Empty()) {
            throw new System.InvalidOperationException("Stack is empty");
        }
        return mainQueue.Peek();
    }
    
    /**
     * Проверяет, пуст ли стек.
     * 
     * @return true, если стек пуст, иначе false
     */
    public bool Empty() {
        return mainQueue.Count == 0;
    }
}

/**
 * Пример использования:
 * 
 * MyStack obj = new MyStack();
 * obj.Push(1);
 * obj.Push(2);
 * int param_2 = obj.Pop();  // 2
 * int param_3 = obj.Top();  // 1
 * bool param_4 = obj.Empty();  // false
 */