impl Solution {
    /**
     * Генерирует треугольник Паскаля заданной высоты.
     * 
     * @param num_rows Количество строк в треугольнике
     * @return Вектор векторов, представляющий треугольник Паскаля
     */
    pub fn generate(num_rows: i32) -> Vec<Vec<i32>> {
        let num_rows = num_rows as usize;
        let mut triangle = Vec::with_capacity(num_rows);
        
        for row_num in 0..num_rows {
            let mut row = vec![1; row_num + 1];
            
            for j in 1..row_num {
                row[j] = triangle[row_num - 1][j - 1] + triangle[row_num - 1][j];
            }
            
            triangle.push(row);
        }
        
        triangle
    }
}