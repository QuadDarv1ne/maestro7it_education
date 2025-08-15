/**
 * https://leetcode.com/problems/valid-parentheses/description/
 */

import java.util.*;

class Solution {
    /**
     * Проверка корректности скобочной последовательности.
     * 
     * Алгоритм:
     * 1. Используем стек для хранения открывающих скобок.
     * 2. При встрече закрывающей — проверяем соответствие с верхом стека.
     * 3. Если стек пуст в конце — последовательность корректна.
     */
    public boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();
        Map<Character, Character> mapping = Map.of(
            ')', '(', 
            ']', '[', 
            '}', '{'
        );

        for (char c : s.toCharArray()) {
            if (mapping.containsValue(c)) {
                stack.push(c);
            } else {
                if (stack.isEmpty() || stack.pop() != mapping.get(c)) {
                    return false;
                }
            }
        }
        return stack.isEmpty();
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