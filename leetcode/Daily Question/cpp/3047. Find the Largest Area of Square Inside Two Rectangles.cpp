/**
 * LeetCode 3047: Find the Largest Area of Square Inside Two Rectangles
 * 
 * Задача: Найти максимальную площадь квадрата, который можно поместить 
 * в пересечение двух прямоугольников.
 * 
 * @param bottomLeft Массив координат левых нижних углов прямоугольников
 * @param topRight Массив координат правых верхних углов прямоугольников
 * @return Максимальная площадь квадрата
 * 
 * Алгоритм:
 * 1. Перебираем все пары прямоугольников O(n²)
 * 2. Для каждой пары находим пересечение прямоугольников
 * 3. В пересечении определяем максимальный квадрат (min из ширины и высоты)
 * 4. Сохраняем максимальную площадь среди всех пар
 * 
 * Временная сложность: O(n²), где n - количество прямоугольников (n ≤ 50)
 * Пространственная сложность: O(1)
 * 
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * - LeetCode задача: https://leetcode.com/problems/find-the-largest-area-of-square-inside-two-rectangles/
 * - Telegram канал: https://t.me/hut_programmer_07
 * - Telegram №1: @quadd4rv1n7
 * - Telegram №2: @dupley_maxim_1999
 * - Rutube: https://rutube.ru/channel/4218729/
 * - Plvideo: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * - YouTube: https://www.youtube.com/@it-coders
 * - ВКонтакте: https://vk.com/science_geeks
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * Находит максимальную площадь квадрата в пересечении двух прямоугольников
     * 
     * @param bottomLeft координаты левых нижних углов прямоугольников
     * @param topRight координаты правых верхних углов прямоугольников
     * @return максимальная площадь квадрата (long long для больших значений)
     */
    long long largestSquareArea(vector<vector<int>>& bottomLeft, vector<vector<int>>& topRight) {
        int n = bottomLeft.size();
        long long maxArea = 0;
        
        // Перебираем все пары прямоугольников
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                // Находим пересечение по оси X
                int x1 = max(bottomLeft[i][0], bottomLeft[j][0]);
                int x2 = min(topRight[i][0], topRight[j][0]);
                
                // Находим пересечение по оси Y
                int y1 = max(bottomLeft[i][1], bottomLeft[j][1]);
                int y2 = min(topRight[i][1], topRight[j][1]);
                
                // Вычисляем ширину и высоту пересечения
                int width = x2 - x1;
                int height = y2 - y1;
                
                // Проверяем существование пересечения и обновляем максимум
                if (width > 0 && height > 0) {
                    long long side = min(width, height);
                    maxArea = max(maxArea, side * side);
                }
            }
        }
        
        return maxArea;
    }
    
private:
    /**
     * Вспомогательная функция: вычисляет пересечение двух прямоугольников
     * 
     * @param bl1 левый нижний угол первого прямоугольника
     * @param tr1 правый верхний угол первого прямоугольника
     * @param bl2 левый нижний угол второго прямоугольника
     * @param tr2 правый верхний угол второго прямоугольника
     * @return площадь максимального квадрата в пересечении
     */
    long long getIntersectionSquareArea(
        const vector<int>& bl1, const vector<int>& tr1,
        const vector<int>& bl2, const vector<int>& tr2
    ) {
        // Пересечение по X
        int x1 = max(bl1[0], bl2[0]);
        int x2 = min(tr1[0], tr2[0]);
        
        // Пересечение по Y
        int y1 = max(bl1[1], bl2[1]);
        int y2 = min(tr1[1], tr2[1]);
        
        // Проверяем существование пересечения
        if (x1 >= x2 || y1 >= y2) {
            return 0;
        }
        
        // Вычисляем сторону квадрата
        long long side = min(x2 - x1, y2 - y1);
        return side * side;
    }
};

// Альтернативное решение с использованием вспомогательной функции
class SolutionWithHelper {
public:
    long long largestSquareArea(vector<vector<int>>& bottomLeft, vector<vector<int>>& topRight) {
        int n = bottomLeft.size();
        long long maxArea = 0;
        
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                long long area = getIntersectionSquareArea(
                    bottomLeft[i], topRight[i],
                    bottomLeft[j], topRight[j]
                );
                maxArea = max(maxArea, area);
            }
        }
        
        return maxArea;
    }
    
private:
    long long getIntersectionSquareArea(
        const vector<int>& bl1, const vector<int>& tr1,
        const vector<int>& bl2, const vector<int>& tr2
    ) {
        int x1 = max(bl1[0], bl2[0]);
        int x2 = min(tr1[0], tr2[0]);
        int y1 = max(bl1[1], bl2[1]);
        int y2 = min(tr1[1], tr2[1]);
        
        if (x1 >= x2 || y1 >= y2) return 0;
        
        long long side = min(x2 - x1, y2 - y1);
        return side * side;
    }
};

/*
 * Примеры использования:
 * 
 * Solution solution;
 * 
 * Пример 1:
 * vector<vector<int>> bottomLeft1 = {{1,1}, {2,2}, {3,1}};
 * vector<vector<int>> topRight1 = {{3,3}, {4,4}, {6,6}};
 * cout << solution.largestSquareArea(bottomLeft1, topRight1) << endl; // Вывод: 1
 * 
 * Пример 2:
 * vector<vector<int>> bottomLeft2 = {{1,1}, {2,2}, {1,2}};
 * vector<vector<int>> topRight2 = {{3,3}, {4,4}, {3,4}};
 * cout << solution.largestSquareArea(bottomLeft2, topRight2) << endl; // Вывод: 1
 * 
 * Пример 3:
 * vector<vector<int>> bottomLeft3 = {{1,1}, {3,3}, {3,1}};
 * vector<vector<int>> topRight3 = {{2,2}, {4,4}, {4,2}};
 * cout << solution.largestSquareArea(bottomLeft3, topRight3) << endl; // Вывод: 0
 * 
 * Ограничения:
 * - n == bottomLeft.length == topRight.length
 * - 2 ≤ n ≤ 50
 * - bottomLeft[i].length == topRight[i].length == 2
 * - 1 ≤ bottomLeft[i][0], bottomLeft[i][1] ≤ 10^7
 * - 1 ≤ topRight[i][0], topRight[i][1] ≤ 10^7
 * - bottomLeft[i][0] < topRight[i][0]
 * - bottomLeft[i][1] < topRight[i][1]
 */