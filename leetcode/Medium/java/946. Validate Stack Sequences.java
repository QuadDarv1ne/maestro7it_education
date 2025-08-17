/**
 * https://leetcode.com/problems/validate-stack-sequences/description/
 */

import java.util.*;

class Solution {
    /**
     * Проверяет, можно ли из последовательности pushed получить последовательность popped
     * с помощью стандартных операций стека (push/pop).
     *
     * @param pushed массив чисел, которые кладутся в стек
     * @param popped массив чисел, которые должны быть извлечены
     * @return true, если последовательность возможна, иначе false
     *
     * Алгоритм:
     * 1. Кладём числа из pushed в стек.
     * 2. Каждый раз, если верхушка стека равна текущему элементу popped, извлекаем.
     * 3. В конце, если весь popped обработан, возвращаем true.
     *
     * Время: O(n), Память: O(n).
     */
    public boolean validateStackSequences(int[] pushed, int[] popped) {
        Deque<Integer> stack = new ArrayDeque<>();
        int j = 0;
        for (int x : pushed) {
            stack.push(x);
            while (!stack.isEmpty() && stack.peek() == popped[j]) {
                stack.pop();
                j++;
            }
        }
        return j == popped.length;
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