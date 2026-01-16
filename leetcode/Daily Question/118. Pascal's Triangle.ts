/**
 * Генерирует треугольник Паскаля заданной высоты.
 * 
 * @param numRows Количество строк в треугольнике
 * @return Двумерный массив, представляющий треугольник Паскаля
 */
function generate(numRows: number): number[][] {
    const triangle: number[][] = [];
    
    for (let rowNum = 0; rowNum < numRows; rowNum++) {
        const row = new Array(rowNum + 1).fill(1);
        
        for (let j = 1; j < rowNum; j++) {
            row[j] = triangle[rowNum - 1][j - 1] + triangle[rowNum - 1][j];
        }
        
        triangle.push(row);
    }
    
    return triangle;
}