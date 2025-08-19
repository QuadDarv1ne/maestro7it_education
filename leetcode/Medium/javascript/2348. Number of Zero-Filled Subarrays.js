/**
 * https://leetcode.com/problems/number-of-zero-filled-subarrays/description/?envType=daily-question&envId=2025-08-19
 */

/**
 * Подсчитывает количество подмассивов, полностью заполненных нулями.
 *
 * Идея:
 * При проходе подсчитываем текущую длину подряд идущих нулей cnt.
 * При встрече нуля добавляем cnt к результату (новые подмассивы, оканчивающиеся здесь).
 *
 * Время: O(n), Память: O(1)
 */
function zeroFilledSubarray(nums) {
    let ans = 0;
    let cnt = 0;
    for (const x of nums) {
        if (x === 0) {
            cnt += 1;
            ans += cnt;
        } else {
            cnt = 0;
        }
    }
    return ans;
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