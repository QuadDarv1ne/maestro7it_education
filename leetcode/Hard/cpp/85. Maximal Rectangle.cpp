/*
https://leetcode.com/problems/maximal-rectangle/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    int maximalRectangle(vector<vector<char>>& matrix) {
        /*
        Решение задачи "Maximal Rectangle" (LeetCode 85).

        Идея:
        - Для каждой строки строим массив высот,
          как в гистограмме.
        - Считаем максимальную площадь для него
          (задача 84).
        
        Сложность:
        - Время: O(m·n)
        - Память: O(n)
        */
        if (matrix.empty() || matrix[0].empty()) return 0;
        int m = matrix.size(), n = matrix[0].size();
        vector<int> heights(n, 0);
        int maxArea = 0;

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] == '1')
                    heights[j]++;
                else
                    heights[j] = 0;
            }
            maxArea = max(maxArea, largestRectangleArea(heights));
        }
        return maxArea;
    }

private:
    int largestRectangleArea(vector<int>& heights) {
        stack<int> st;
        heights.push_back(0);
        int maxArea = 0;

        for (int i = 0; i < heights.size(); i++) {
            while (!st.empty() && heights[st.top()] > heights[i]) {
                int height = heights[st.top()]; st.pop();
                int width = st.empty() ? i : i - st.top() - 1;
                maxArea = max(maxArea, height * width);
            }
            st.push(i);
        }
        heights.pop_back();
        return maxArea;
    }
};
