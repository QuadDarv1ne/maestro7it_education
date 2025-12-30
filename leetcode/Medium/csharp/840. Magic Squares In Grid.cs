/**
 * https://leetcode.com/problems/magic-squares-in-grid/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Magic Squares In Grid"
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

using System;
using System.Collections.Generic;

public class Solution {
    /**
     * Подсчитывает количество магических квадратов 3x3 в заданной сетке.
     * 
     * @param grid двумерный массив целых чисел
     * @return количество магических квадратов 3x3 в сетке
     * 
     * Магический квадрат 3x3 должен удовлетворять:
     * 1. Содержать все числа от 1 до 9 (без повторений)
     * 2. Суммы строк, столбцов и диагоналей равны 15
     */
    public int NumMagicSquaresInside(int[][] grid) {
        int rows = grid.Length;
        int cols = grid[0].Length;
        
        // Если сетка меньше чем 3x3, не может быть магических квадратов
        if (rows < 3 || cols < 3) {
            return 0;
        }
        
        int count = 0;
        
        // Перебираем все возможные левые верхние углы квадратов 3x3
        for (int r = 0; r <= rows - 3; r++) {
            for (int c = 0; c <= cols - 3; c++) {
                // Оптимизация: центр магического квадрата 3x3 всегда должен быть 5
                if (grid[r + 1][c + 1] != 5) {
                    continue;
                }
                if (IsMagic(grid, r, c)) {
                    count++;
                }
            }
        }
        
        return count;
    }
    
    /**
     * Проверяет, является ли подматрица 3x3 магическим квадратом.
     * 
     * @param grid исходная сетка
     * @param r начальная строка
     * @param c начальный столбец
     * @return true если подматрица является магическим квадратом
     */
    private bool IsMagic(int[][] grid, int r, int c) {
        // Проверяем, что все числа от 1 до 9 без повторений
        var nums = new HashSet<int>();
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                int num = grid[r + i][c + j];
                if (num < 1 || num > 9) {
                    return false;
                }
                nums.Add(num);
            }
        }
        
        if (nums.Count != 9) {
            return false;
        }
        
        // Проверяем суммы строк (должны быть равны 15)
        for (int i = 0; i < 3; i++) {
            int rowSum = 0;
            for (int j = 0; j < 3; j++) {
                rowSum += grid[r + i][c + j];
            }
            if (rowSum != 15) {
                return false;
            }
        }
        
        // Проверяем суммы столбцов
        for (int j = 0; j < 3; j++) {
            int colSum = 0;
            for (int i = 0; i < 3; i++) {
                colSum += grid[r + i][c + j];
            }
            if (colSum != 15) {
                return false;
            }
        }
        
        // Проверяем диагонали
        int diag1 = grid[r][c] + grid[r + 1][c + 1] + grid[r + 2][c + 2];
        int diag2 = grid[r][c + 2] + grid[r + 1][c + 1] + grid[r + 2][c];
        
        return diag1 == 15 && diag2 == 15;
    }
}