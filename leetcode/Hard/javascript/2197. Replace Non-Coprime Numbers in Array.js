/*
 https://leetcode.com/problems/replace-non-coprime-numbers-in-array/description/?envType=daily-question&envId=2025-09-16
*/

/**
 * Заменяет соседние числа массива на их НОК,
 * если они не являются взаимно простыми.
 *
 * Алгоритм:
 * 1. Используется массив как стек.
 * 2. Проверяем верхний элемент стека.
 * 3. Если НОД > 1, заменяем числа их НОК.
 * 4. Иначе добавляем текущее число.
 *
 * Пример:
 *   Ввод:  [6, 4, 3, 2, 1]
 *   Вывод: [12, 1]
 *
 * @param {number[]} nums входной массив
 * @return {number[]} массив после всех замен
 */
var replaceNonCoprimes = function(nums) {
    const gcd = (a, b) => {
        while (b !== 0) {
            [a, b] = [b, a % b];
        }
        return a;
    };

    let stack = [];
    for (let num of nums) {
        while (stack.length > 0) {
            let g = gcd(stack[stack.length - 1], num);
            if (g > 1) {
                num = (stack.pop() * num) / g;
            } else break;
        }
        stack.push(num);
    }
    return stack;
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
