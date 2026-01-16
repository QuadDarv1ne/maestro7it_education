import java.util.ArrayList;
import java.util.List;

class Solution {
    /**
     * Генерирует треугольник Паскаля заданной высоты
     * 
     * @param numRows Количество строк в треугольнике
     * @return Список списков, представляющий треугольник Паскаля
     * 
     * Сложность: O(n²), где n = numRows
     * 
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
    public List<List<Integer>> generate(int numRows) {
        List<List<Integer>> triangle = new ArrayList<>();
        
        for (int rowNum = 0; rowNum < numRows; rowNum++) {
            List<Integer> row = new ArrayList<>();
            
            for (int j = 0; j <= rowNum; j++) {
                if (j == 0 || j == rowNum) {
                    row.add(1);
                } else {
                    int sum = triangle.get(rowNum - 1).get(j - 1) + 
                              triangle.get(rowNum - 1).get(j);
                    row.add(sum);
                }
            }
            
            triangle.add(row);
        }
        
        return triangle;
    }
}