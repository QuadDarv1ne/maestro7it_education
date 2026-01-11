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

public class Solution {
    public int MaximalRectangle(char[][] matrix) {
        if (matrix.Length == 0 || matrix[0].Length == 0) return 0;
        
        int rows = matrix.Length;
        int cols = matrix[0].Length;
        int maxArea = 0;
        
        // Массив высот для каждого столбца
        int[] heights = new int[cols];
        
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
            maxArea = Math.Max(maxArea, LargestRectangleArea(heights));
        }
        
        return maxArea;
    }
    
    // Функция для нахождения максимальной площади в гистограмме
    private int LargestRectangleArea(int[] heights) {
        int n = heights.Length;
        Stack<int> stack = new Stack<int>();
        int maxArea = 0;
        
        for (int i = 0; i <= n; i++) {
            // Барьерное значение 0 в конце для обработки оставшихся элементов
            int h = (i == n) ? 0 : heights[i];
            
            // Пока стек не пуст и текущая высота меньше высоты в стеке
            while (stack.Count > 0 && h < heights[stack.Peek()]) {
                int height = heights[stack.Pop()];
                int width = stack.Count == 0 ? i : i - stack.Peek() - 1;
                maxArea = Math.Max(maxArea, height * width);
            }
            
            stack.Push(i);
        }
        
        return maxArea;
    }
}