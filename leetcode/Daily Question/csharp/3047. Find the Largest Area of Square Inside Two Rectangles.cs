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

using System;

public class Solution 
{
    /// <summary>
    /// Находит максимальную площадь квадрата, который можно поместить в пересечение двух прямоугольников
    /// </summary>
    /// <param name="bottomLeft">Массив координат левых нижних углов прямоугольников</param>
    /// <param name="topRight">Массив координат правых верхних углов прямоугольников</param>
    /// <returns>Максимальная площадь квадрата (long для больших значений)</returns>
    /// <remarks>
    /// Алгоритм перебирает все возможные пары прямоугольников и находит
    /// максимальный квадрат, который помещается в их пересечении.
    /// </remarks>
    public long LargestSquareArea(int[][] bottomLeft, int[][] topRight) 
    {
        int n = bottomLeft.Length;
        long maxArea = 0;
        
        // Перебираем все пары прямоугольников
        for (int i = 0; i < n - 1; i++) 
        {
            for (int j = i + 1; j < n; j++) 
            {
                // Находим пересечение по оси X
                int x1 = Math.Max(bottomLeft[i][0], bottomLeft[j][0]);
                int x2 = Math.Min(topRight[i][0], topRight[j][0]);
                
                // Находим пересечение по оси Y
                int y1 = Math.Max(bottomLeft[i][1], bottomLeft[j][1]);
                int y2 = Math.Min(topRight[i][1], topRight[j][1]);
                
                // Вычисляем ширину и высоту пересечения
                int width = x2 - x1;
                int height = y2 - y1;
                
                // Проверяем существование пересечения и обновляем максимум
                if (width > 0 && height > 0) 
                {
                    long side = Math.Min(width, height);
                    maxArea = Math.Max(maxArea, side * side);
                }
            }
        }
        
        return maxArea;
    }
    
    /// <summary>
    /// Вспомогательная функция: вычисляет площадь максимального квадрата в пересечении двух прямоугольников
    /// </summary>
    /// <param name="bl1">Левый нижний угол первого прямоугольника</param>
    /// <param name="tr1">Правый верхний угол первого прямоугольника</param>
    /// <param name="bl2">Левый нижний угол второго прямоугольника</param>
    /// <param name="tr2">Правый верхний угол второго прямоугольника</param>
    /// <returns>Площадь максимального квадрата или 0, если пересечения нет</returns>
    private long GetIntersectionSquareArea(int[] bl1, int[] tr1, int[] bl2, int[] tr2)
    {
        // Пересечение по X
        int x1 = Math.Max(bl1[0], bl2[0]);
        int x2 = Math.Min(tr1[0], tr2[0]);
        
        // Пересечение по Y
        int y1 = Math.Max(bl1[1], bl2[1]);
        int y2 = Math.Min(tr1[1], tr2[1]);
        
        // Проверяем существование пересечения
        if (x1 >= x2 || y1 >= y2)
        {
            return 0;
        }
        
        // Вычисляем сторону квадрата
        long side = Math.Min(x2 - x1, y2 - y1);
        return side * side;
    }
}

/// <summary>
/// Альтернативное решение с использованием вспомогательной функции
/// </summary>
public class SolutionWithHelper
{
    public long LargestSquareArea(int[][] bottomLeft, int[][] topRight) 
    {
        int n = bottomLeft.Length;
        long maxArea = 0;
        
        for (int i = 0; i < n - 1; i++) 
        {
            for (int j = i + 1; j < n; j++) 
            {
                long area = GetIntersectionSquareArea(
                    bottomLeft[i], topRight[i],
                    bottomLeft[j], topRight[j]
                );
                maxArea = Math.Max(maxArea, area);
            }
        }
        
        return maxArea;
    }
    
    private long GetIntersectionSquareArea(int[] bl1, int[] tr1, int[] bl2, int[] tr2)
    {
        int x1 = Math.Max(bl1[0], bl2[0]);
        int x2 = Math.Min(tr1[0], tr2[0]);
        int y1 = Math.Max(bl1[1], bl2[1]);
        int y2 = Math.Min(tr1[1], tr2[1]);
        
        if (x1 >= x2 || y1 >= y2) return 0;
        
        long side = Math.Min(x2 - x1, y2 - y1);
        return side * side;
    }
}

/*
 * Примеры использования:
 * 
 * var solution = new Solution();
 * 
 * Пример 1:
 * int[][] bottomLeft1 = new int[][] { new int[] {1,1}, new int[] {2,2}, new int[] {3,1} };
 * int[][] topRight1 = new int[][] { new int[] {3,3}, new int[] {4,4}, new int[] {6,6} };
 * Console.WriteLine(solution.LargestSquareArea(bottomLeft1, topRight1)); // Вывод: 1
 *
 * Пример 2:
 * int[][] bottomLeft2 = new int[][] { new int[] {1,1}, new int[] {2,2}, new int[] {1,2} };
 * int[][] topRight2 = new int[][] { new int[] {3,3}, new int[] {4,4}, new int[] {3,4} };
 * Console.WriteLine(solution.LargestSquareArea(bottomLeft2, topRight2)); // Вывод: 1
 *
 * Пример 3:
 * int[][] bottomLeft3 = new int[][] { new int[] {1,1}, new int[] {3,3}, new int[] {3,1} };
 * int[][] topRight3 = new int[][] { new int[] {2,2}, new int[] {4,4}, new int[] {4,2} };
 * Console.WriteLine(solution.LargestSquareArea(bottomLeft3, topRight3)); // Вывод: 0
 * 
 * Тестирование с большими значениями:
 * int[][] bottomLeft4 = new int[][] { new int[] {10000,10000}, new int[] {20000,20000} };
 * int[][] topRight4 = new int[][] { new int[] {60000,60000}, new int[] {70000,70000} };
 * Console.WriteLine(solution.LargestSquareArea(bottomLeft4, topRight4)); // Вывод: 2500000000
 * 
 * Ограничения:
 * - n == bottomLeft.Length == topRight.Length
 * - 2 ≤ n ≤ 50
 * - bottomLeft[i].Length == topRight[i].Length == 2
 * - 1 ≤ bottomLeft[i][0], bottomLeft[i][1] ≤ 10^7
 * - 1 ≤ topRight[i][0], topRight[i][1] ≤ 10^7
 * - bottomLeft[i][0] < topRight[i][0]
 * - bottomLeft[i][1] < topRight[i][1]
 */