/*
https://leetcode.com/problems/largest-rectangle-in-histogram/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        /*
        Решение задачи "Largest Rectangle in Histogram" (LeetCode 84).

        Идея:
        - Используем стек для хранения индексов с возрастающими
          высотами.
        - Когда высота падает, вычисляем площадь для элементов стека.
        - В конец добавляем 0 для очистки всех оставшихся.
        
        Сложность:
        - Время: O(n)
        - Память: O(n)
        */
        stack<int> st;
        heights.push_back(0); // фиктивный барьер
        int maxArea = 0;

        for (int i = 0; i < heights.size(); ++i) {
            while (!st.empty() && heights[st.top()] > heights[i]) {
                int h = heights[st.top()];
                st.pop();
                int w = st.empty() ? i : i - st.top() - 1;
                maxArea = max(maxArea, h * w);
            }
            st.push(i);
        }
        return maxArea;
    }
};
