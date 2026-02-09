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

#include <queue>

using namespace std;

class MyStack {
private:
    queue<int> mainQueue;   // Основная очередь
    queue<int> tempQueue;   // Временная очередь
    
public:
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
    MyStack() {
        // Конструктор: инициализация пустых очередей
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
    void push(int x) {
        // Добавляем новый элемент во временную очередь
        tempQueue.push(x);
        
        // Перемещаем все элементы из основной очереди во временную
        while (!mainQueue.empty()) {
            tempQueue.push(mainQueue.front());
            mainQueue.pop();
        }
        
        // Меняем очереди местами
        swap(mainQueue, tempQueue);
    }
    
    /**
     * Удаляет элемент с вершины стека и возвращает его.
     * 
     * @return Элемент с вершины стека
     * @throws runtime_error Если стек пуст
     */
    int pop() {
        if (empty()) {
            throw runtime_error("Stack is empty");
        }
        int result = mainQueue.front();
        mainQueue.pop();
        return result;
    }
    
    /**
     * Возвращает элемент на вершине стека без удаления.
     * 
     * @return Элемент на вершине стека
     * @throws runtime_error Если стек пуст
     */
    int top() {
        if (empty()) {
            throw runtime_error("Stack is empty");
        }
        return mainQueue.front();
    }
    
    /**
     * Проверяет, пуст ли стек.
     * 
     * @return true, если стек пуст, иначе false
     */
    bool empty() {
        return mainQueue.empty();
    }
};

/**
 * Пример использования:
 * 
 * MyStack* obj = new MyStack();
 * obj->push(1);
 * obj->push(2);
 * int param_2 = obj->pop();  // 2
 * int param_3 = obj->top();  // 1
 * bool param_4 = obj->empty();  // false
 */