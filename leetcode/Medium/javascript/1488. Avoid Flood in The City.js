/*
https://leetcode.com/problems/avoid-flood-in-the-city/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

/**
 * Решение задачи "Avoid Flood in The City" (LeetCode 1488).
 *
 * Идея:
 * - lastRain хранит последний индекс дождя над озером.
 * - dryDays (массив + сортировка или min-heap) хранит индексы сухих дней.
 * - При дожде над уже полным озером ищем ближайший сухой день для осушения.
 *
 * @param {number[]} rains
 * @return {number[]}
 */
var avoidFlood = function(rains) {
    const lastRain = new Map();
    const dryDays = [];
    const res = Array(rains.length).fill(-1);

    for(let i=0;i<rains.length;i++){
        const lake = rains[i];
        if(lake === 0){
            dryDays.push(i);
            res[i] = 1;
        } else {
            if(lastRain.has(lake)){
                // ищем первый dryDay > lastRain[lake]
                let idx = dryDays.findIndex(d => d > lastRain.get(lake));
                if(idx === -1) return [];
                let dryIdx = dryDays[idx];
                res[dryIdx] = lake;
                dryDays.splice(idx,1);
            }
            lastRain.set(lake,i);
            res[i] = -1;
        }
    }
    return res;
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