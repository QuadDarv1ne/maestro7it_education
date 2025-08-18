/**
 * https://leetcode.com/problems/24-game/description/
 */

/**
 * Оценивает, можно ли из карт составить выражение, равное 24, используя +, -, *, / и скобки.
 *
 * @param {number[]} cards — массив из 4 чисел [1..9]
 * @return {boolean} — true, если выражение существует; иначе false
 *
 * Используется рекурсивный бэктрекинг: выбираем пару чисел,
 * применяем все операции, рекурсивно проверяем результат.
 */
var judgePoint24 = function(cards) {
    const EPS = 1e-6;
    function backtrack(nums) {
        if (nums.length === 1) {
            return Math.abs(nums[0] - 24) < EPS;
        }
        for (let i = 0; i < nums.length; i++) {
            for (let j = i + 1; j < nums.length; j++) {
                const rest = [];
                for (let k = 0; k < nums.length; k++) {
                    if (k !== i && k !== j) rest.push(nums[k]);
                }
                const a = nums[i], b = nums[j];
                const candidates = [a + b, a - b, b - a, a * b];
                if (Math.abs(b) > EPS) candidates.push(a / b);
                if (Math.abs(a) > EPS) candidates.push(b / a);

                for (const cand of candidates) {
                    if (backtrack([...rest, cand])) return true;
                }
            }
        }
        return false;
    }
    return backtrack(cards.map(n => n * 1.0));
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