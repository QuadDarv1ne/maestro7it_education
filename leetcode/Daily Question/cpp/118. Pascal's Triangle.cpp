#include <vector>
using namespace std;

class Solution {
public:
    /**
     * Генерирует треугольник Паскаля заданной высоты
     * 
     * @param numRows Количество строк в треугольнике
     * @return Вектор векторов, представляющий треугольник Паскаля
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
    vector<vector<int>> generate(int numRows) {
        vector<vector<int>> triangle;
        
        for (int rowNum = 0; rowNum < numRows; rowNum++) {
            vector<int> row(rowNum + 1, 1);
            
            for (int j = 1; j < rowNum; j++) {
                row[j] = triangle[rowNum - 1][j - 1] + triangle[rowNum - 1][j];
            }
            
            triangle.push_back(row);
        }
        
        return triangle;
    }
};