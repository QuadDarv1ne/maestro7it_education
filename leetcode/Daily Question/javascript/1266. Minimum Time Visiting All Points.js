/**
 * Находит минимальное время для посещения всех точек в заданном порядке
 * 
 * @param {number[][]} points Массив точек в формате [x, y] в порядке посещения
 * @return {number} Минимальное время для посещения всех точек
 * 
 * Сложность: Время O(n), Память O(1)
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
 */

/**
 * @param {number[][]} points
 * @return {number}
 */
var minTimeToVisitAllPoints = function(points) {
    let totalTime = 0;
    
    // Проходим по всем соседним парам точек
    for (let i = 0; i < points.length - 1; i++) {
        const dx = Math.abs(points[i + 1][0] - points[i][0]);
        const dy = Math.abs(points[i + 1][1] - points[i][1]);
        
        // Минимальное время между точками - максимум из разностей координат
        totalTime += Math.max(dx, dy);
    }
    
    return totalTime;
};