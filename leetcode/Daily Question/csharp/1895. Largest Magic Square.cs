public class Solution {
    public int LargestMagicSquare(int[][] grid) {
        int rows = grid.Length;
        int cols = grid[0].Length;
        
        // Префиксные суммы по строкам
        int[][] rowPrefix = new int[rows][];
        for (int i = 0; i < rows; i++) {
            rowPrefix[i] = new int[cols + 1];
            for (int j = 0; j < cols; j++) {
                rowPrefix[i][j + 1] = rowPrefix[i][j] + grid[i][j];
            }
        }
        
        // Префиксные суммы по столбцам
        int[][] colPrefix = new int[cols][];
        for (int j = 0; j < cols; j++) {
            colPrefix[j] = new int[rows + 1];
            for (int i = 0; i < rows; i++) {
                colPrefix[j][i + 1] = colPrefix[j][i] + grid[i][j];
            }
        }
        
        // Проверяем квадраты от максимального до минимального размера
        for (int size = Math.Min(rows, cols); size >= 1; size--) {
            for (int i = 0; i <= rows - size; i++) {
                for (int j = 0; j <= cols - size; j++) {
                    if (IsMagicSquare(grid, i, j, size, rowPrefix, colPrefix)) {
                        return size;
                    }
                }
            }
        }
        
        return 1; // Минимальный волшебный квадрат 1×1
    }
    
    private bool IsMagicSquare(int[][] grid, int startI, int startJ, int size, 
                               int[][] rowPrefix, int[][] colPrefix) {
        int? targetSum = null;
        
        // Проверяем суммы строк
        for (int i = startI; i < startI + size; i++) {
            int rowSum = rowPrefix[i][startJ + size] - rowPrefix[i][startJ];
            if (targetSum == null) {
                targetSum = rowSum;
            } else if (rowSum != targetSum) {
                return false;
            }
        }
        
        // Проверяем суммы столбцов
        for (int j = startJ; j < startJ + size; j++) {
            int colSum = colPrefix[j][startI + size] - colPrefix[j][startI];
            if (colSum != targetSum) {
                return false;
            }
        }
        
        // Проверяем главную диагональ
        int diag1Sum = 0;
        for (int k = 0; k < size; k++) {
            diag1Sum += grid[startI + k][startJ + k];
        }
        if (diag1Sum != targetSum) {
            return false;
        }
        
        // Проверяем побочную диагональ
        int diag2Sum = 0;
        for (int k = 0; k < size; k++) {
            diag2Sum += grid[startI + k][startJ + size - 1 - k];
        }
        return diag2Sum == targetSum;
    }
}