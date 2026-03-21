/**
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

class Solution {
    public int[][] reverseSubmatrix(int[][] grid, int x, int y, int k) {
        // Используем два указателя: верхнюю и нижнюю строки подматрицы
        int top = x;
        int bottom = x + k - 1;
        
        // Меняем строки местами, пока указатели не встретятся
        while (top < bottom) {
            // Меняем местами строки top и bottom в пределах столбцов от y до y + k - 1
            for (int col = y; col < y + k; ++col) {
                int temp = grid[top][col];
                grid[top][col] = grid[bottom][col];
                grid[bottom][col] = temp;
            }
            ++top;
            --bottom;
        }
        
        return grid;
    }
}