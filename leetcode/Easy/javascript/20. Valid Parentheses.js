/**
 * https://leetcode.com/problems/valid-parentheses/description/
 */

/**
 * Проверка корректности скобочной последовательности.
 * 
 * Алгоритм:
 * 1. Стек хранит открывающие скобки.
 * 2. При встрече закрывающей — проверяем соответствие с верхом стека.
 * 3. В конце стек должен быть пуст.
 * 
 * @param {string} s - строка, содержащая только '()[]{}'
 * @return {boolean} true — если корректна, иначе false
 */
var isValid = function(s) {
    const stack = [];
    const mapping = { ')': '(', ']': '[', '}': '{' };

    for (const char of s) {
        if (Object.values(mapping).includes(char)) {
            stack.push(char);
        } else {
            if (stack.length === 0 || stack.pop() !== mapping[char]) {
                return false;
            }
        }
    }
    return stack.length === 0;
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