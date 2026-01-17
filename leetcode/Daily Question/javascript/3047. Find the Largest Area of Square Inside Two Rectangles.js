/**
 * LeetCode 3047: Find the Largest Area of Square Inside Two Rectangles
 * 
 * Задача: Найти максимальную площадь квадрата, который можно поместить 
 * в пересечение двух прямоугольников.
 * 
 * @param {number[][]} bottomLeft - Массив координат левых нижних углов прямоугольников
 * @param {number[][]} topRight - Массив координат правых верхних углов прямоугольников
 * @return {number} Максимальная площадь квадрата
 * 
 * Алгоритм:
 * 1. Перебираем все пары прямоугольников O(n²)
 * 2. Для каждой пары находим пересечение прямоугольников
 * 3. В пересечении определяем максимальный квадрат (min из ширины и высоты)
 * 4. Сохраняем максимальную площадь среди всех пар
 * 
 * Временная сложность: O(n²), где n - количество прямоугольников
 * Пространственная сложность: O(1)
 * 
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * - LeetCode задача: https://leetcode.com/problems/find-the-largest-area-of-square-inside-two-rectangles/
 * - Telegram канал: https://t.me/hut_programmer_07
 * - Rutube: https://rutube.ru/channel/4218729/
 * - YouTube: https://www.youtube.com/@it-coders
 * - ВКонтакте: https://vk.com/science_geeks
 */

/**
 * @param {number[][]} bottomLeft
 * @param {number[][]} topRight
 * @return {number}
 */
var largestSquareArea = function(bottomLeft, topRight) {
    const n = bottomLeft.length;
    let maxArea = 0;
    
    // Перебираем все пары прямоугольников
    for (let i = 0; i < n - 1; i++) {
        for (let j = i + 1; j < n; j++) {
            // Находим пересечение по оси X
            const x1 = Math.max(bottomLeft[i][0], bottomLeft[j][0]);
            const x2 = Math.min(topRight[i][0], topRight[j][0]);
            
            // Находим пересечение по оси Y
            const y1 = Math.max(bottomLeft[i][1], bottomLeft[j][1]);
            const y2 = Math.min(topRight[i][1], topRight[j][1]);
            
            // Вычисляем ширину и высоту пересечения
            const width = x2 - x1;
            const height = y2 - y1;
            
            // Проверяем существование пересечения и обновляем максимум
            if (width > 0 && height > 0) {
                const side = Math.min(width, height);
                maxArea = Math.max(maxArea, side * side);
            }
        }
    }
    
    return maxArea;
};