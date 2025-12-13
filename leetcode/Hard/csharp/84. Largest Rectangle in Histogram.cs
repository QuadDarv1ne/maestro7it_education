/*
https://leetcode.com/problems/largest-rectangle-in-histogram/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public int LargestRectangleArea(int[] heights) {
        /*
        Решение задачи "Largest Rectangle in Histogram" (LeetCode 84).

        Идея:
        - Стек хранит индексы с неубывающими высотами.
        - При падении высоты считаем прямоугольники.
        - В конец добавляем 0, чтобы очистить стек.

        Сложность:
        - Время: O(n)
        - Память: O(n)
        */
        var stack = new Stack<int>();
        int maxArea = 0;

        // Общий массив + фиктивная 0 высота
        var list = new List<int>(heights);
        list.Add(0);

        for (int i = 0; i < list.Count; i++) {
            while (stack.Count > 0 && list[stack.Peek()] > list[i]) {
                int height = list[stack.Pop()];
                int width = stack.Count == 0 ? i : i - stack.Peek() - 1;
                maxArea = Math.Max(maxArea, height * width);
            }
            stack.Push(i);
        }
        return maxArea;
    }
}
