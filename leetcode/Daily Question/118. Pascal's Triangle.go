/**
 * Генерирует треугольник Паскаля заданной высоты.
 * 
 * @param numRows Количество строк в треугольнике
 * @return Двумерный срез, представляющий треугольник Паскаля
 */
func generate(numRows int) [][]int {
    triangle := make([][]int, numRows)
    
    for rowNum := 0; rowNum < numRows; rowNum++ {
        row := make([]int, rowNum+1)
        row[0], row[rowNum] = 1, 1
        
        for j := 1; j < rowNum; j++ {
            row[j] = triangle[rowNum-1][j-1] + triangle[rowNum-1][j]
        }
        
        triangle[rowNum] = row
    }
    
    return triangle
}