/**
 * Автор: Дуплей Максим Игоревич - AGLA
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
    /**
     * Проверяет, содержится ли целевое значение в отсортированной матрице.
     * 
     * Алгоритм (поиск из правого верхнего угла):
     * 1. Начинаем с правого верхнего угла матрицы (row=0, col=n-1).
     * 2. Сравниваем текущий элемент с целевым значением:
     *    - Если matrix[row][col] == target: возвращаем true
     *    - Если matrix[row][col] > target: двигаемся влево (col--)
     *    - Если matrix[row][col] < target: двигаемся вниз (row++)
     * 3. Повторяем, пока не выйдем за границы матрицы.
     * 
     * Сложность:
     * Время: O(m + n)
     * Пространство: O(1)
     * 
     * @param matrix Двумерная матрица, отсортированная по строкам и столбцам
     * @param target Искомое значение
     * @return true, если target найден в матрице, иначе false
     * 
     * Пример:
     * Матрица:
     * [
     *   [1,   4,  7, 11, 15],
     *   [2,   5,  8, 12, 19],
     *   [3,   6,  9, 16, 22],
     *   [10, 13, 14, 17, 24],
     *   [18, 21, 23, 26, 30]
     * ]
     * 
     * searchMatrix(matrix, 5) → true
     * searchMatrix(matrix, 20) → false
     */
    public boolean searchMatrix(int[][] matrix, int target) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return false;
        }
        
        int m = matrix.length;
        int n = matrix[0].length;
        
        // Начинаем с правого верхнего угла
        int row = 0, col = n - 1;
        
        while (row < m && col >= 0) {
            int current = matrix[row][col];
            if (current == target) {
                return true;
            } else if (current > target) {
                // Текущий элемент слишком большой, двигаемся влево
                col--;
            } else {
                // Текущий элемент слишком маленький, двигаемся вниз
                row++;
            }
        }
        
        return false;
    }
    
    /**
     * Альтернативная реализация: поиск из левого нижнего угла.
     */
    public boolean searchMatrixFromLeftBottom(int[][] matrix, int target) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return false;
        }
        
        int m = matrix.length;
        int n = matrix[0].length;
        
        // Начинаем с левого нижнего угла
        int row = m - 1, col = 0;
        
        while (row >= 0 && col < n) {
            int current = matrix[row][col];
            if (current == target) {
                return true;
            } else if (current > target) {
                // Текущий элемент слишком большой, двигаемся вверх
                row--;
            } else {
                // Текущий элемент слишком маленький, двигаемся вправо
                col++;
            }
        }
        
        return false;
    }
}