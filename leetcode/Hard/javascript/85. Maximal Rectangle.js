/*
https://leetcode.com/problems/maximal-rectangle/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var maximalRectangle = function(matrix) {
    /*
    Решение задачи "Maximal Rectangle" (LeetCode 85).

    Идея:
    - Для каждой строки накапливаем высоты гистограммы.
    - Затем считаем максимальную площадь (задача 84).
    
    Сложность:
    - Время: O(m·n)
    - Память: O(n)
    */
    if (!matrix || matrix.length === 0) return 0;

    let maxArea = 0;
    let n = matrix[0].length;
    let heights = Array(n).fill(0);

    for (let row of matrix) {
        for (let i = 0; i < n; i++) {
            heights[i] = row[i] === '1' ? heights[i] + 1 : 0;
        }
        maxArea = Math.max(maxArea, largestRectangleArea(heights));
    }
    return maxArea;
};

function largestRectangleArea(heights) {
    let stack = [];
    let maxArea = 0;
    heights.push(0);

    for (let i = 0; i < heights.length; i++) {
        while (stack.length && heights[stack[stack.length - 1]] > heights[i]) {
            let height = heights[stack.pop()];
            let width = stack.length === 0 ? i : i - stack[stack.length - 1] - 1;
            maxArea = Math.max(maxArea, height * width);
        }
        stack.push(i);
    }
    heights.pop();
    return maxArea;
}
