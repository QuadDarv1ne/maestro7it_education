/**
 * https://leetcode.com/problems/alice-and-bob-playing-flower-game/description/?envType=daily-question&envId=2025-08-29
 */

// JavaScript (для LeetCode)
var flowerGame = function(n, m) {
    // Alice выигрывает, если сумма x + y нечётна
    const x_even = Math.floor(n / 2);
    const x_odd  = Math.ceil(n / 2);
    const y_even = Math.floor(m / 2);
    const y_odd  = Math.ceil(m / 2);
    return x_even * y_odd + x_odd * y_even;
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/