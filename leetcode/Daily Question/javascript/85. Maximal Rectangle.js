/**
 * Находит площадь максимального прямоугольника, состоящего из единиц
 * 
 * @param {character[][]} matrix Бинарная матрица (из символов '0' и '1')
 * @return {number} Площадь максимального прямоугольника из единиц
 * 
 * Сложность: Время O(rows * cols), Память O(cols)
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
 * @param {character[][]} matrix
 * @return {number}
 */
var maximalRectangle = function(matrix) {
    if (!matrix.length || !matrix[0].length) return 0;
    
    const rows = matrix.length;
    const cols = matrix[0].length;
    let maxArea = 0;
    
    // Массив высот для каждого столбца
    const heights = new Array(cols).fill(0);
    
    for (let i = 0; i < rows; i++) {
        // Обновляем высоты для текущей строки
        for (let j = 0; j < cols; j++) {
            if (matrix[i][j] === '1') {
                heights[j] += 1;
            } else {
                heights[j] = 0;
            }
        }
        
        // Находим максимальную площадь в гистограмме
        maxArea = Math.max(maxArea, largestRectangleArea(heights));
    }
    
    return maxArea;
};

// Функция для нахождения максимальной площади в гистограмме
function largestRectangleArea(heights) {
    const n = heights.length;
    const stack = [];
    let maxArea = 0;
    
    for (let i = 0; i <= n; i++) {
        // Барьерное значение 0 в конце для обработки оставшихся элементов
        const h = (i === n) ? 0 : heights[i];
        
        // Пока стек не пуст и текущая высота меньше высоты в стеке
        while (stack.length > 0 && h < heights[stack[stack.length - 1]]) {
            const height = heights[stack.pop()];
            const width = stack.length === 0 ? i : i - stack[stack.length - 1] - 1;
            maxArea = Math.max(maxArea, height * width);
        }
        
        stack.push(i);
    }
    
    return maxArea;
}