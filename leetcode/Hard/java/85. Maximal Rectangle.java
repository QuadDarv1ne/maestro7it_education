/*
https://leetcode.com/problems/maximal-rectangle/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
    public int maximalRectangle(char[][] matrix) {
        /*
        Решение задачи "Maximal Rectangle" (LeetCode 85).

        Идея:
        - Строим для каждой строки гистограмму высот.
        - Для каждой гистограммы считаем максимальную
          площадь (задача 84).

        Сложность:
        - Время: O(m·n)
        - Память: O(n)
        */
        if (matrix == null || matrix.length == 0) return 0;
        int m = matrix.length, n = matrix[0].length;
        int maxArea = 0;
        int[] heights = new int[n];

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                heights[j] = matrix[i][j] == '1' ? heights[j] + 1 : 0;
            }
            maxArea = Math.max(maxArea, largestRectangleArea(heights));
        }
        return maxArea;
    }

    private int largestRectangleArea(int[] heights) {
        Stack<Integer> st = new Stack<>();
        int maxArea = 0;
        int[] arr = Arrays.copyOf(heights, heights.length + 1);
        arr[arr.length - 1] = 0;

        for (int i = 0; i < arr.length; i++) {
            while (!st.isEmpty() && arr[st.peek()] > arr[i]) {
                int height = arr[st.pop()];
                int width = st.isEmpty() ? i : i - st.peek() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            st.push(i);
        }
        return maxArea;
    }
}
