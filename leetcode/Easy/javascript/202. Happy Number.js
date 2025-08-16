/**
 * https://leetcode.com/problems/happy-number/description/
 */

/**
 * Проверяет, является ли число счастливым.
 * Счастливое число — это число, которое после многократной замены на сумму квадратов его цифр 
 * в итоге становится равным 1. Если процесс попадает в цикл — число не счастливое.
 *
 * @param {number} n
 * @return {boolean}
 */
var isHappy = function(n) {
    const seen = new Set();
    while (n !== 1 && !seen.has(n)) {
        seen.add(n);
        let next = 0;
        while (n > 0) {
            let d = n % 10;
            next += d * d;
            n = Math.floor(n / 10);
        }
        n = next;
    }
    return n === 1;
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