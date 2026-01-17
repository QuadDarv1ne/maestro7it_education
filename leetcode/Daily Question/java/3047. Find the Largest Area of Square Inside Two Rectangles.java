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

class Solution {
    /**
     * Находит максимальную площадь квадрата, который можно поместить в пересечение двух прямоугольников
     * 
     * @param bottomLeft массив координат левых нижних углов прямоугольников
     * @param topRight массив координат правых верхних углов прямоугольников
     * @return максимальная площадь квадрата (long для больших значений)
     */
    public long largestSquareArea(int[][] bottomLeft, int[][] topRight) {
        int n = bottomLeft.length;
        long maxArea = 0;
        
        // Перебираем все пары прямоугольников
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                // Находим пересечение по оси X
                int x1 = Math.max(bottomLeft[i][0], bottomLeft[j][0]);
                int x2 = Math.min(topRight[i][0], topRight[j][0]);
                
                // Находим пересечение по оси Y
                int y1 = Math.max(bottomLeft[i][1], bottomLeft[j][1]);
                int y2 = Math.min(topRight[i][1], topRight[j][1]);
                
                // Вычисляем ширину и высоту пересечения
                int width = x2 - x1;
                int height = y2 - y1;
                
                // Проверяем существование пересечения и обновляем максимум
                if (width > 0 && height > 0) {
                    long side = Math.min(width, height);
                    maxArea = Math.max(maxArea, side * side);
                }
            }
        }
        
        return maxArea;
    }
    
    /**
     * Вспомогательная функция: вычисляет площадь максимального квадрата в пересечении двух прямоугольников
     * 
     * @param bl1 левый нижний угол первого прямоугольника
     * @param tr1 правый верхний угол первого прямоугольника
     * @param bl2 левый нижний угол второго прямоугольника
     * @param tr2 правый верхний угол второго прямоугольника
     * @return площадь максимального квадрата или 0, если пересечения нет
     */
    private long getIntersectionSquareArea(int[] bl1, int[] tr1, int[] bl2, int[] tr2) {
        // Пересечение по X
        int x1 = Math.max(bl1[0], bl2[0]);
        int x2 = Math.min(tr1[0], tr2[0]);
        
        // Пересечение по Y
        int y1 = Math.max(bl1[1], bl2[1]);
        int y2 = Math.min(tr1[1], tr2[1]);
        
        // Проверяем существование пересечения
        if (x1 >= x2 || y1 >= y2) {
            return 0;
        }
        
        // Вычисляем сторону квадрата
        long side = Math.min(x2 - x1, y2 - y1);
        return side * side;
    }
}

/**
 * Альтернативное решение с использованием вспомогательной функции
 */
class SolutionWithHelper {
    public long largestSquareArea(int[][] bottomLeft, int[][] topRight) {
        int n = bottomLeft.length;
        long maxArea = 0;
        
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                long area = getIntersectionSquareArea(
                    bottomLeft[i], topRight[i],
                    bottomLeft[j], topRight[j]
                );
                maxArea = Math.max(maxArea, area);
            }
        }
        
        return maxArea;
    }
    
    private long getIntersectionSquareArea(int[] bl1, int[] tr1, int[] bl2, int[] tr2) {
        int x1 = Math.max(bl1[0], bl2[0]);
        int x2 = Math.min(tr1[0], tr2[0]);
        int y1 = Math.max(bl1[1], bl2[1]);
        int y2 = Math.min(tr1[1], tr2[1]);
        
        if (x1 >= x2 || y1 >= y2) return 0;
        
        long side = Math.min(x2 - x1, y2 - y1);
        return side * side;
    }
}

/**
 * Компактное решение в функциональном стиле (Java 8+)
 */
class SolutionFunctional {
    public long largestSquareArea(int[][] bottomLeft, int[][] topRight) {
        int n = bottomLeft.length;
        long maxArea = 0;
        
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                int width = Math.min(topRight[i][0], topRight[j][0]) - 
                           Math.max(bottomLeft[i][0], bottomLeft[j][0]);
                int height = Math.min(topRight[i][1], topRight[j][1]) - 
                            Math.max(bottomLeft[i][1], bottomLeft[j][1]);
                
                if (width > 0 && height > 0) {
                    long side = Math.min(width, height);
                    maxArea = Math.max(maxArea, side * side);
                }
            }
        }
        
        return maxArea;
    }
}

/**
 * Класс для тестирования решения
 */
class Main {
    /**
     * Метод для тестирования решения
     */
    public static void main(String[] args) {
        Solution solution = new Solution();
        
        // Пример 1
        int[][] bottomLeft1 = {{1,1}, {2,2}, {3,1}};
        int[][] topRight1 = {{3,3}, {4,4}, {6,6}};
        System.out.println("Пример 1: " + solution.largestSquareArea(bottomLeft1, topRight1)); // Вывод: 1
        
        // Пример 2
        int[][] bottomLeft2 = {{1,1}, {2,2}, {1,2}};
        int[][] topRight2 = {{3,3}, {4,4}, {3,4}};
        System.out.println("Пример 2: " + solution.largestSquareArea(bottomLeft2, topRight2)); // Вывод: 1
        
        // Пример 3
        int[][] bottomLeft3 = {{1,1}, {3,3}, {3,1}};
        int[][] topRight3 = {{2,2}, {4,4}, {4,2}};
        System.out.println("Пример 3: " + solution.largestSquareArea(bottomLeft3, topRight3)); // Вывод: 0
        
        // Пример с большими значениями
        int[][] bottomLeft4 = {{10000,10000}, {20000,20000}};
        int[][] topRight4 = {{60000,60000}, {70000,70000}};
        System.out.println("Пример 4: " + solution.largestSquareArea(bottomLeft4, topRight4)); // Вывод: 2500000000
        
        // Тестирование производительности
        long startTime = System.nanoTime();
        solution.largestSquareArea(bottomLeft1, topRight1);
        long endTime = System.nanoTime();
        System.out.println("Время выполнения: " + (endTime - startTime) / 1000000.0 + " мс");
    }
}

/*
 * Ограничения:
 * - n == bottomLeft.length == topRight.length
 * - 2 ≤ n ≤ 50
 * - bottomLeft[i].length == topRight[i].length == 2
 * - 1 ≤ bottomLeft[i][0], bottomLeft[i][1] ≤ 10^7
 * - 1 ≤ topRight[i][0], topRight[i][1] ≤ 10^7
 * - bottomLeft[i][0] < topRight[i][0]
 * - bottomLeft[i][1] < topRight[i][1]
 * 
 * Примечания:
 * - Используется long вместо int для площади, так как максимальная площадь 
 *   может достигать (10^7)^2 = 10^14, что превышает максимальное значение int
 * - Алгоритм проверяет все возможные пары прямоугольников, что дает O(n²) сложность
 * - Для каждой пары вычисляется пересечение и находится максимальный квадрат
 */