/**
 * https://leetcode.com/problems/implement-queue-using-stacks/description/
 */

using System.Collections.Generic;

public class MyQueue {
    private Stack<int> inStack;
    private Stack<int> outStack;

    public MyQueue() {
        inStack = new Stack<int>();
        outStack = new Stack<int>();
    }

    public void Push(int x) {
        inStack.Push(x);
    }

    public int Pop() {
        MoveIfNeeded();
        return outStack.Pop();
    }

    public int Peek() {
        MoveIfNeeded();
        return outStack.Peek();
    }

    public bool Empty() {
        return inStack.Count == 0 && outStack.Count == 0;
    }

    private void MoveIfNeeded() {
        if (outStack.Count == 0) {
            while (inStack.Count > 0) {
                outStack.Push(inStack.Pop());
            }
        }
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