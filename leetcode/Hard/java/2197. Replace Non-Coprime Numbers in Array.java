/*
 https://leetcode.com/problems/replace-non-coprime-numbers-in-array/description/?envType=daily-question&envId=2025-09-16
*/

import java.util.*;

class Solution {
    /**
     * Заменяет соседние числа массива на их НОК,
     * если они не являются взаимно простыми.
     *
     * Алгоритм:
     * 1. Используется ArrayList как стек.
     * 2. Проверяется верхний элемент стека.
     * 3. Если НОД > 1, заменяем числа их НОК.
     * 4. Иначе добавляем текущее число.
     *
     * Пример:
     *   Ввод:  [6, 4, 3, 2, 1]
     *   Вывод: [12, 1]
     *
     * @param nums входной массив
     * @return массив после всех замен
     */
    public List<Integer> replaceNonCoprimes(int[] nums) {
        List<Integer> stack = new ArrayList<>();
        for (int val : nums) {
            long num = val;
            while (!stack.isEmpty()) {
                int g = gcd(stack.get(stack.size() - 1), (int)num);
                if (g > 1) {
                    num = (long)stack.get(stack.size() - 1) * num / g;
                    stack.remove(stack.size() - 1);
                } else break;
            }
            stack.add((int)num);
        }
        return stack;
    }

    private int gcd(int a, int b) {
        while (b != 0) {
            int t = a % b;
            a = b;
            b = t;
        }
        return a;
    }
}

/* Полезные ссылки:
 1. Telegram ❃ Хижина программиста Æ:   https://t.me/hut_programmer_07
 2. Telegram №1 @quadd4rv1n7
 3. Telegram №2 @dupley_maxim_1999
 4. Rutube канал: https://rutube.ru/channel/4218729/
 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 6. YouTube канал: https://www.youtube.com/@it-coders
 7. ВК группа: https://vk.com/science_geeks
*/
