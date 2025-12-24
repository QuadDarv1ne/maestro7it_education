/**
 * Задача: Два лучших непересекающихся события (LeetCode #2054)
 * https://leetcode.com/problems/two-best-non-overlapping-events/
 * 
 * Описание:
 * Дан массив событий events, где events[i] = [startTime_i, endTime_i, value_i].
 * Каждое событие имеет время начала, время окончания и ценность.
 * Необходимо выбрать не более двух непересекающихся событий, чтобы максимизировать сумму их ценностей.
 * События не пересекаются, если конец первого события строго меньше начала второго (включительно: end < start).
 * 
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 * 
 * Сложность:
 * - Время: O(n log n) из-за сортировки и бинарного поиска
 * - Память: O(n) для хранения отсортированных массивов и префиксных максимумов
 */

var maxTwoEvents = function(events) {
    const n = events.length;
    
    // Сортируем события по времени окончания
    const eventsByEnd = [...events].sort((a, b) => a[1] - b[1]);
    
    // Создаем массивы времен окончания и префиксных максимумов
    const endTimes = new Array(n);
    const prefixMax = new Array(n);
    
    for (let i = 0; i < n; i++) {
        endTimes[i] = eventsByEnd[i][1];
        if (i === 0) {
            prefixMax[i] = eventsByEnd[i][2];
        } else {
            prefixMax[i] = Math.max(prefixMax[i-1], eventsByEnd[i][2]);
        }
    }
    
    // Находим максимальную ценность одного события
    let maxValue = 0;
    for (const event of events) {
        maxValue = Math.max(maxValue, event[2]);
    }
    
    // Перебираем каждое событие как второе
    for (const event of events) {
        const start = event[0];
        const value = event[2];
        
        // Бинарный поиск последнего события, которое заканчивается до start
        let left = 0, right = n;
        while (left < right) {
            const mid = Math.floor((left + right) / 2);
            if (endTimes[mid] < start) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        const idx = left - 1;
        
        if (idx >= 0) {
            maxValue = Math.max(maxValue, prefixMax[idx] + value);
        }
    }
    
    return maxValue;
};