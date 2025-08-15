/**
 * https://leetcode.com/problems/implement-queue-using-stacks/description/
 */

#include <stack>
using namespace std;

class MyQueue {
private:
    stack<int> in_stack, out_stack;

    void shiftStacks() {
        if (out_stack.empty()) {
            while (!in_stack.empty()) {
                out_stack.push(in_stack.top());
                in_stack.pop();
            }
        }
    }

public:
    MyQueue() {}

    void push(int x) {
        in_stack.push(x);
    }

    int pop() {
        shiftStacks();
        int val = out_stack.top();
        out_stack.pop();
        return val;
    }

    int peek() {
        shiftStacks();
        return out_stack.top();
    }

    bool empty() {
        return in_stack.empty() && out_stack.empty();
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