/**
 * https://leetcode.com/problems/min-stack/description/
 */

#include <stack>
#include <algorithm>
using namespace std;

class MinStack {
private:
    stack<int> stk;      // основной стек
    stack<int> minStk;   // стек минимумов

public:
    /**
     * Конструктор: создаёт пустой стек.
     */
    MinStack() {}

    /**
     * Добавляет элемент val в стек.
     * Если стек минимумов пуст или val <= текущего минимума,
     * в стек минимумов помещается val, иначе — текущий минимум.
     */
    void push(int val) {
        stk.push(val);
        if (minStk.empty() || val <= minStk.top())
            minStk.push(val);
        else
            minStk.push(minStk.top());
    }

    /**
     * Удаляет верхний элемент из обоих стеков.
     */
    void pop() {
        stk.pop();
        minStk.pop();
    }

    /**
     * Возвращает верхний элемент основного стека.
     */
    int top() {
        return stk.top();
    }

    /**
     * Возвращает текущий минимальный элемент стека.
     */
    int getMin() {
        return minStk.top();
    }
};

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