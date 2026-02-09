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

import java.util.LinkedList;
import java.util.Queue;

class MyStack {
    private Queue<Integer> mainQueue;
    private Queue<Integer> tempQueue;
    
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
        mainQueue = new LinkedList<>();
        tempQueue = new LinkedList<>();
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
    public void push(int x) {
        // Добавляем новый элемент во временную очередь
        tempQueue.offer(x);
        
        // Перемещаем все элементы из основной очереди во временную
        while (!mainQueue.isEmpty()) {
            tempQueue.offer(mainQueue.poll());
        }
        
        // Меняем очереди местами
        Queue<Integer> temp = mainQueue;
        mainQueue = tempQueue;
        tempQueue = temp;
    }
    
    /**
     * Удаляет элемент с вершины стека и возвращает его.
     * 
     * @return Элемент с вершины стека
     * @throws IllegalStateException Если стек пуст
     */
    public int pop() {
        if (empty()) {
            throw new IllegalStateException("Stack is empty");
        }
        return mainQueue.poll();
    }
    
    /**
     * Возвращает элемент на вершине стека без удаления.
     * 
     * @return Элемент на вершине стека
     * @throws IllegalStateException Если стек пуст
     */
    public int top() {
        if (empty()) {
            throw new IllegalStateException("Stack is empty");
        }
        return mainQueue.peek();
    }
    
    /**
     * Проверяет, пуст ли стек.
     * 
     * @return true, если стек пуст, иначе false
     */
    public boolean empty() {
        return mainQueue.isEmpty();
    }
}

/**
 * Пример использования:
 * 
 * MyStack obj = new MyStack();
 * obj.push(1);
 * obj.push(2);
 * int param_2 = obj.pop();  // 2
 * int param_3 = obj.top();  // 1
 * boolean param_4 = obj.empty();  // false
 */