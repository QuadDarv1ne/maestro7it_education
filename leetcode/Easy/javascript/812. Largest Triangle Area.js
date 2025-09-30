/**
 * https://leetcode.com/problems/largest-triangle-area/description/?envType=daily-question&envId=2025-09-27
 */

/**
 * @param {number[][]} points
 * @return {number}
 */
var largestTriangleArea = function(points) {
    let n = points.length;
    let ans = 0.0;
    for (let i = 0; i < n; i++) {
        let [x1, y1] = points[i];
        for (let j = i + 1; j < n; j++) {
            let [x2, y2] = points[j];
            for (let k = j + 1; k < n; k++) {
                let [x3, y3] = points[k];
                let cross = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1);
                let area = Math.abs(cross) / 2.0;
                if (area > ans) {
                    ans = area;
                }
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