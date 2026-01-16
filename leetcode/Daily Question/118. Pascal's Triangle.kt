class Solution {
    /**
     * Генерирует треугольник Паскаля заданной высоты.
     * 
     * @param numRows Количество строк в треугольнике
     * @return Список списков, представляющий треугольник Паскаля
     */
    fun generate(numRows: Int): List<List<Int>> {
        val triangle = mutableListOf<List<Int>>()
        
        for (rowNum in 0 until numRows) {
            val row = mutableListOf<Int>()
            
            for (j in 0..rowNum) {
                if (j == 0 || j == rowNum) {
                    row.add(1)
                } else {
                    val sum = triangle[rowNum - 1][j - 1] + triangle[rowNum - 1][j]
                    row.add(sum)
                }
            }
            
            triangle.add(row)
        }
        
        return triangle
    }
}