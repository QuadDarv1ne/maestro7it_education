/**
 * Автор: Дуплей Максим Игоревич - AGLA
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
 */

/**
 * Находит минимальное время завершения одного наземного и одного водного аттракциона.
 * 
 * Турист должен посетить ровно один наземный и ровно один водный аттракцион
 * в любом порядке. Аттракцион можно начать в момент его открытия или позже.
 * Если аттракцион начат в момент t, он заканчивается в t + duration.
 * После завершения одного аттракциона можно сразу начать другой или подождать его открытия.
 * 
 * Алгоритм:
 * 1. Рассматриваем оба порядка: land→water и water→land
 * 2. Для каждого аттракциона первого типа находим оптимальный аттракцион второго типа
 * 3. Используем формулу: finish = max(first_end, second_start) + second_duration
 * 4. Сортируем аттракционы второго типа по времени начала
 * 5. Строим префиксные минимумы длительностей и суффиксные минимумы времени завершения
 * 6. Для каждого первого аттракциона бинарным поиском находим границу
 *    и за O(1) получаем оптимальное время
 * 
 * @param {number[]} landStartTime - Времена открытия наземных аттракционов
 * @param {number[]} landDuration - Длительности наземных аттракционов
 * @param {number[]} waterStartTime - Времена открытия водных аттракционов
 * @param {number[]} waterDuration - Длительности водных аттракционов
 * @return {number} Минимальное возможное время завершения обоих аттракционов
 * 
 * Временная сложность: O(N log M + M log M)
 * Пространственная сложность: O(N + M)
 * 
 * Пример:
 * landStartTime = [2, 8], landDuration = [4, 1]
 * waterStartTime = [6], waterDuration = [3]
 * Результат: 9
 */
var earliestFinishTime = function(landStartTime, landDuration, waterStartTime, waterDuration) {
    /**
     * Вычисляет минимальное время для порядка: сначала first, потом second.
     * 
     * Для каждого аттракциона первого типа перебираем все возможные
     * аттракционы второго типа и находим минимальное время завершения.
     * Оптимизация достигается за счёт сортировки и предподсчёта минимумов.
     * 
     * @param {number[]} firstStart - Времена открытия аттракционов первого типа
     * @param {number[]} firstDur - Длительности аттракционов первого типа
     * @param {number[]} secondStart - Времена открытия аттракционов второго типа
     * @param {number[]} secondDur - Длительности аттракционов второго типа
     * @return {number} Минимальное время завершения для данного порядка
     */
    function solve(firstStart, firstDur, secondStart, secondDur) {
        const n = firstStart.length;
        const m = secondStart.length;
        
        // Создаём массив аттракционов второго типа: [start, duration]
        const second = [];
        for (let i = 0; i < m; i++) {
            second.push([secondStart[i], secondDur[i]]);
        }
        
        // Сортируем по времени начала
        second.sort((a, b) => a[0] - b[0]);
        
        // Массив времён начала для бинарного поиска
        const starts = second.map(s => s[0]);
        
        // Префиксный минимум длительностей
        // prefMinDur[i] = минимальная длительность среди первых i аттракционов
        const prefMinDur = new Array(m + 1).fill(Infinity);
        for (let i = 0; i < m; i++) {
            prefMinDur[i + 1] = Math.min(prefMinDur[i], second[i][1]);
        }
        
        // Суффиксный минимум времён завершения
        // suffMinFinish[i] = минимальное время завершения среди аттракционов с индексом >= i
        const suffMinFinish = new Array(m + 1).fill(Infinity);
        for (let i = m - 1; i >= 0; i--) {
            const finish = second[i][0] + second[i][1];
            suffMinFinish[i] = Math.min(suffMinFinish[i + 1], finish);
        }
        
        let ans = Infinity;
        
        for (let i = 0; i < n; i++) {
            // Время завершения первого аттракциона
            const firstEnd = firstStart[i] + firstDur[i];
            
            // Бинарный поиск: находим первый second, у которого start >= firstEnd
            let left = 0;
            let right = m;
            while (left < right) {
                const mid = (left + right) >> 1;
                if (starts[mid] >= firstEnd) {
                    right = mid;
                } else {
                    left = mid + 1;
                }
            }
            const idx = left;
            
            // Случай 1: second начинается после завершения first
            // finish = second_finish
            if (idx < m) {
                ans = Math.min(ans, suffMinFinish[idx]);
            }
            
            // Случай 2: second уже открыт к моменту завершения first
            // finish = firstEnd + second_duration
            if (idx > 0) {
                ans = Math.min(ans, firstEnd + prefMinDur[idx]);
            }
        }
        
        return ans;
    }
    
    // Вычисляем минимальное время для обоих порядков
    const landFirst = solve(landStartTime, landDuration, waterStartTime, waterDuration);
    const waterFirst = solve(waterStartTime, waterDuration, landStartTime, landDuration);
    
    return Math.min(landFirst, waterFirst);
};