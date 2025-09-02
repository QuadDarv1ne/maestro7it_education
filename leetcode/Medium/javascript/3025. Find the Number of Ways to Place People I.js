/**
 * https://leetcode.com/problems/find-the-number-of-ways-to-place-people-i/description/?envType=daily-question&envId=2025-09-02
 */

/**
 * Задача:
 * Найти количество способов выбрать упорядоченные пары точек (i, j),
 * такие что:
 * 1) x1 <= x2 и y1 >= y2
 * 2) в прямоугольнике, образованном (x1, y1) и (x2, y2), нет других точек
 *
 * @param {number[][]} points - массив точек [x, y]
 * @return {number} количество допустимых пар
 */
var numberOfPairs = function(points) {
    let n = points.length;
    let ans = 0;

    for (let i = 0; i < n; i++) {
        let [x1, y1] = points[i];
        for (let j = 0; j < n; j++) {
            if (i === j) continue;
            let [x2, y2] = points[j];
            if (x1 <= x2 && y1 >= y2) {
                let blocked = false;
                for (let k = 0; k < n; k++) {
                    if (k === i || k === j) continue;
                    let [xk, yk] = points[k];
                    if (x1 <= xk && xk <= x2 && y2 <= yk && yk <= y1) {
                        blocked = true;
                        break;
                    }
                }
                if (!blocked) ans++;
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