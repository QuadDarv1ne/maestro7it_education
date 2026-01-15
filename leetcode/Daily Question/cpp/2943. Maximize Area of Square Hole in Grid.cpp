/**
 * Максимальная площадь квадратного отверстия в сетке
 * 
 * @param n Количество горизонтальных интервалов
 * @param m Количество вертикальных интервалов
 * @param hBars Горизонтальные удаленные перемычки
 * @param vBars Вертикальные удаленные перемычки
 * @return Максимальная площадь квадратного отверстия
 * 
 * Сложность: O(h log h + v log v) время, O(1) дополнительная память
 */
class Solution {
public:
    int maximizeSquareHoleArea(int n, int m, vector<int>& hBars, vector<int>& vBars) {
        // Сортируем массивы
        sort(hBars.begin(), hBars.end());
        sort(vBars.begin(), vBars.end());
        
        // Находим максимальный непрерывный промежуток в горизонталях
        int maxHGap = 1;
        int current = 1;
        for (int i = 1; i < hBars.size(); i++) {
            if (hBars[i] == hBars[i-1] + 1) {
                current++;
            } else {
                maxHGap = max(maxHGap, current);
                current = 1;
            }
        }
        maxHGap = max(maxHGap, current);
        
        // Находим максимальный непрерывный промежуток в вертикалях
        int maxVGap = 1;
        current = 1;
        for (int i = 1; i < vBars.size(); i++) {
            if (vBars[i] == vBars[i-1] + 1) {
                current++;
            } else {
                maxVGap = max(maxVGap, current);
                current = 1;
            }
        }
        maxVGap = max(maxVGap, current);
        
        // Добавляем 1, так как k промежутков дают отверстие размера k+1
        int side = min(maxHGap, maxVGap) + 1;
        return side * side;
    }
};