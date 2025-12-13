/*
https://leetcode.com/problems/maximal-rectangle/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public int MaximalRectangle(char[][] matrix) {
        /*
        Решение задачи "Maximal Rectangle" (LeetCode 85).

        Идея:
        - Для каждой строки накапливаем высоты '1'.
        - Вычисляем максимальную площадь по гистограмме
          (задача 84).
        
        Сложность:
        - Время: O(m·n)
        - Память: O(n)
        */
        if (matrix == null || matrix.Length == 0) return 0;
        
        int m = matrix.Length;
        int n = matrix[0].Length;
        int maxArea = 0;
        int[] heights = new int[n];

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                heights[j] = matrix[i][j] == '1' ? heights[j] + 1 : 0;
            }
            maxArea = Math.Max(maxArea, LargestRectangleArea(heights));
        }
        return maxArea;
    }

    private int LargestRectangleArea(int[] heights) {
        var st = new Stack<int>();
        int maxArea = 0;
        var list = new List<int>(heights);
        list.Add(0);

        for (int i = 0; i < list.Count; i++) {
            while (st.Count > 0 && list[st.Peek()] > list[i]) {
                int height = list[st.Pop()];
                int width = st.Count == 0 ? i : i - st.Peek() - 1;
                maxArea = Math.Max(maxArea, height * width);
            }
            st.Push(i);
        }
        return maxArea;
    }
}
