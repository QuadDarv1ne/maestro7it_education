/**
 * https://leetcode.com/problems/climbing-stairs/description/
 */

/**
 * Вычисляет число способов подняться на вершину лестницы из n ступеней,
 * при условии, что можно подниматься на 1 или 2 ступени за ход.
 *
 * Используется оптимизированное динамическое программирование по Фибоначчи:
 * ways[n] = ways[n-1] + ways[n-2], храним только два предыдущих значения.
 *
 * @param {number} n Количество ступеней
 * @return {number} Число способов подняться на n ступеней
 * Время: O(n), Память: O(1)
 */
var climbStairs = function(n) {
    if (n <= 1) return 1;
    let first = 1, second = 2;
    for (let i = 3; i <= n; i++) {
        [first, second] = [second, first + second];
    }
    return second;
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