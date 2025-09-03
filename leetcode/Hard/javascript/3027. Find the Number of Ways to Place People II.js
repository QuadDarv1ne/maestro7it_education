/**
 * https://leetcode.com/problems/find-the-number-of-ways-to-place-people-ii/description/?envType=daily-question&envId=2025-09-03
 */

/**
 * @param {number[][]} points
 * @return {number}
 * Возвращает количество пар (Alice, Bob), отвечающих условиям задачи.
 */
var numberOfPairs = function(points) {
    // Сортировка: по x ↑, при равных x — y ↓
    points.sort((a, b) => a[0] === b[0] ? b[1] - a[1] : a[0] - b[0]);
    let ans = 0;
    const n = points.length;
    for (let i = 0; i < n; i++) {
        let maxY = -Infinity;
        const y1 = points[i][1];
        for (let j = i + 1; j < n; j++) {
            const y2 = points[j][1];
            if (maxY < y2 && y2 <= y1) {
                ans++;
                maxY = y2;
            }
        }
    }
    return ans;
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