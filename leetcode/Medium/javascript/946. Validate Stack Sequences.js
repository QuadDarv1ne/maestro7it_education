/**
 * https://leetcode.com/problems/validate-stack-sequences/description/
 */

/**
 * Проверяет корректность последовательности popped
 * относительно pushed при моделировании стека.
 *
 * @param {number[]} pushed - массив чисел, которые по очереди кладутся в стек
 * @param {number[]} popped - массив чисел, которые должны быть извлечены
 * @return {boolean} true, если последовательность возможна, иначе false
 *
 * Алгоритм:
 * 1. Идём по pushed и кладём элементы в стек.
 * 2. Если верхушка совпадает с popped[j], извлекаем и двигаем j.
 * 3. В конце проверяем, совпадает ли количество извлечённых элементов.
 *
 * Сложность: O(n) по времени и O(n) по памяти.
 */
var validateStackSequences = function(pushed, popped) {
    const stack = [];
    let j = 0;
    for (const x of pushed) {
        stack.push(x);
        while (stack.length && stack[stack.length - 1] === popped[j]) {
            stack.pop();
            j++;
        }
    }
    return j === popped.length;
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