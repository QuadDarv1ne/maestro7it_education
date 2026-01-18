class Solution {
public:
    int largestMagicSquare(vector<vector<int>>& grid) {
        int rows = grid.size();
        int cols = grid[0].size();
        
        // Префиксные суммы по строкам
        vector<vector<int>> rowPrefix(rows, vector<int>(cols + 1, 0));
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                rowPrefix[i][j + 1] = rowPrefix[i][j] + grid[i][j];
            }
        }
        
        // Префиксные суммы по столбцам
        vector<vector<int>> colPrefix(cols, vector<int>(rows + 1, 0));
        for (int j = 0; j < cols; j++) {
            for (int i = 0; i < rows; i++) {
                colPrefix[j][i + 1] = colPrefix[j][i] + grid[i][j];
            }
        }
        
        // Проверяем квадраты от максимального до минимального размера
        for (int size = min(rows, cols); size >= 1; size--) {
            for (int i = 0; i <= rows - size; i++) {
                for (int j = 0; j <= cols - size; j++) {
                    if (isMagicSquare(grid, i, j, size, rowPrefix, colPrefix)) {
                        return size;
                    }
                }
            }
        }
        
        return 1; // Минимальный волшебный квадрат 1×1
    }
    
private:
    bool isMagicSquare(vector<vector<int>>& grid, int startI, int startJ, int size,
                       vector<vector<int>>& rowPrefix, vector<vector<int>>& colPrefix) {
        int targetSum = -1;
        
        // Проверяем суммы строк
        for (int i = startI; i < startI + size; i++) {
            int rowSum = rowPrefix[i][startJ + size] - rowPrefix[i][startJ];
            if (targetSum == -1) {
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
};