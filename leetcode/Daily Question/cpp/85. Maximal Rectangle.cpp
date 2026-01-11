/**
 * Находит площадь максимального прямоугольника, состоящего из единиц
 * 
 * @param matrix Бинарная матрица (из символов '0' и '1')
 * @return Площадь максимального прямоугольника из единиц
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

class Solution {
public:
    int maximalRectangle(vector<vector<char>>& matrix) {
        if (matrix.empty() || matrix[0].empty()) return 0;
        
        int rows = matrix.size();
        int cols = matrix[0].size();
        int maxArea = 0;
        
        // Массив высот для каждого столбца
        vector<int> heights(cols, 0);
        
        for (int i = 0; i < rows; i++) {
            // Обновляем высоты для текущей строки
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == '1') {
                    heights[j] += 1;
                } else {
                    heights[j] = 0;
                }
            }
            
            // Находим максимальную площадь в гистограмме
            maxArea = max(maxArea, largestRectangleArea(heights));
        }
        
        return maxArea;
    }

private:
    // Функция для нахождения максимальной площади в гистограмме
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size();
        stack<int> st;
        int maxArea = 0;
        
        for (int i = 0; i <= n; i++) {
            // Барьерное значение -1 в конце для обработки оставшихся элементов
            int h = (i == n) ? 0 : heights[i];
            
            // Пока стек не пуст и текущая высота меньше высоты в стеке
            while (!st.empty() && h < heights[st.top()]) {
                int height = heights[st.top()];
                st.pop();
                int width = st.empty() ? i : i - st.top() - 1;
                maxArea = max(maxArea, height * width);
            }
            
            st.push(i);
        }
        
        return maxArea;
    }
};