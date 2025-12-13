/*
https://leetcode.com/problems/largest-rectangle-in-histogram/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
    public int largestRectangleArea(int[] heights) {
        /*
        Решение задачи "Largest Rectangle in Histogram" (LeetCode 84).

        Идея:
        - Стек хранит индексы с неубывающими высотами.
        - При уменьшении высоты вычисляем площадь.
        - В конец добавляем 0 для полной обработки.

        Сложность:
        - Время: O(n)
        - Память: O(n)
        */
        Stack<Integer> st = new Stack<>();
        int maxArea = 0;

        // Увеличенная последовательность с 0 в конце
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
