/*
 https://leetcode.com/problems/replace-non-coprime-numbers-in-array/description/?envType=daily-question&envId=2025-09-16
*/

#include <vector>
using namespace std;

class Solution {
public:
    /**
     * Заменяет соседние числа массива на их НОК,
     * если они не являются взаимно простыми.
     *
     * Алгоритм:
     * 1. Используется вектор в качестве стека.
     * 2. Для каждого числа проверяется верхний элемент стека.
     * 3. Если НОД > 1, заменяем числа их НОК.
     * 4. Иначе добавляем текущее число в стек.
     *
     * Пример:
     *   Ввод:  [6, 4, 3, 2, 1]
     *   Вывод: [12, 1]
     *
     * @param nums входной массив
     * @return массив после всех замен
     */
    vector<int> replaceNonCoprimes(vector<int>& nums) {
        auto gcd = [](long long a, long long b) {
            while (b != 0) {
                long long t = a % b;
                a = b;
                b = t;
            }
            return (int)a;
        };

        vector<int> stack;
        for (int num : nums) {
            long long cur = num;
            while (!stack.empty()) {
                int g = gcd(stack.back(), cur);
                if (g > 1) {
                    cur = (long long)stack.back() * cur / g;
                    stack.pop_back();
                } else break;
            }
            stack.push_back((int)cur);
        }
        return stack;
    }
};

/* Полезные ссылки:
 1. Telegram ❃ Хижина программиста Æ:   https://t.me/hut_programmer_07
 2. Telegram №1 @quadd4rv1n7
 3. Telegram №2 @dupley_maxim_1999
 4. Rutube канал: https://rutube.ru/channel/4218729/
 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 6. YouTube канал: https://www.youtube.com/@it-coders
 7. ВК группа: https://vk.com/science_geeks
*/
