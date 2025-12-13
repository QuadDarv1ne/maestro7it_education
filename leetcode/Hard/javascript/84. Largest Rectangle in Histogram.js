/*
https://leetcode.com/problems/largest-rectangle-in-histogram/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var largestRectangleArea = function(heights) {
    /*
    Решение задачи "Largest Rectangle in Histogram" (LeetCode 84).

    Идея:
    - Стек с индексами по неубывающей высоте.
    - При падении высоты считаем площадь.
    - Добавляем 0 в конец для полной очистки стека.

    Сложность:
    - Время: O(n)
    - Память: O(n)
    */
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
    return maxArea;
};
