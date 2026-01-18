var largestMagicSquare = function(grid) {
    const rows = grid.length;
    const cols = grid[0].length;
    
    // Префиксные суммы по строкам
    const rowPrefix = new Array(rows);
    for (let i = 0; i < rows; i++) {
        rowPrefix[i] = new Array(cols + 1).fill(0);
        for (let j = 0; j < cols; j++) {
            rowPrefix[i][j + 1] = rowPrefix[i][j] + grid[i][j];
        }
    }
    
    // Префиксные суммы по столбцам
    const colPrefix = new Array(cols);
    for (let j = 0; j < cols; j++) {
        colPrefix[j] = new Array(rows + 1).fill(0);
        for (let i = 0; i < rows; i++) {
            colPrefix[j][i + 1] = colPrefix[j][i] + grid[i][j];
        }
    }
    
    // Проверяем квадраты от максимального до минимального размера
    for (let size = Math.min(rows, cols); size >= 1; size--) {
        for (let i = 0; i <= rows - size; i++) {
            for (let j = 0; j <= cols - size; j++) {
                if (isMagicSquare(grid, i, j, size, rowPrefix, colPrefix)) {
                    return size;
                }
            }
        }
    }
    
    return 1; // Минимальный волшебный квадрат 1×1
};

function isMagicSquare(grid, startI, startJ, size, rowPrefix, colPrefix) {
    let targetSum = null;
    
    // Проверяем суммы строк
    for (let i = startI; i < startI + size; i++) {
        const rowSum = rowPrefix[i][startJ + size] - rowPrefix[i][startJ];
        if (targetSum === null) {
            targetSum = rowSum;
        } else if (rowSum !== targetSum) {
            return false;
        }
    }
    
    // Проверяем суммы столбцов
    for (let j = startJ; j < startJ + size; j++) {
        const colSum = colPrefix[j][startI + size] - colPrefix[j][startI];
        if (colSum !== targetSum) {
            return false;
        }
    }
    
    // Проверяем главную диагональ
    let diag1Sum = 0;
    for (let k = 0; k < size; k++) {
        diag1Sum += grid[startI + k][startJ + k];
    }
    if (diag1Sum !== targetSum) {
        return false;
    }
    
    // Проверяем побочную диагональ
    let diag2Sum = 0;
    for (let k = 0; k < size; k++) {
        diag2Sum += grid[startI + k][startJ + size - 1 - k];
    }
    return diag2Sum === targetSum;
}