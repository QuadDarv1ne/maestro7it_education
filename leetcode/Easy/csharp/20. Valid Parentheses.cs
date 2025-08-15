/**
 * https://leetcode.com/problems/valid-parentheses/description/
 */

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Проверка корректности скобочной последовательности.
    /// Алгоритм:
    /// 1. Стек хранит открывающие скобки.
    /// 2. При встрече закрывающей скобки проверяем соответствие с верхом стека.
    /// 3. В конце стек должен быть пуст.
    /// </summary>
    public bool IsValid(string s) {
        Stack<char> stack = new Stack<char>();
        Dictionary<char, char> mapping = new Dictionary<char, char> {
            { ')', '(' },
            { ']', '[' },
            { '}', '{' }
        };

        foreach (char c in s) {
            if (mapping.ContainsValue(c)) {
                stack.Push(c);
            } else {
                if (stack.Count == 0 || stack.Pop() != mapping[c]) {
                    return false;
                }
            }
        }
        return stack.Count == 0;
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