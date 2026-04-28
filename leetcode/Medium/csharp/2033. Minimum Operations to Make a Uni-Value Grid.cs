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

public class Solution {
    /*
     * Возвращает минимальное количество операций для приведения
     * двумерной сетки grid к uni-value (все элементы равны).
     * 
     * За одну операцию можно прибавить x или вычесть x из любого элемента.
     * Если это невозможно, возвращает -1.
     *
     * https://leetcode.com/problems/minimum-operations-to-make-a-uni-value-grid/description/?envType=daily-question&envId=2026-04-28
     *
     * @param grid двумерный массив целых чисел
     * @param x    целое число, шаг изменения элементов
     * @return     минимальное число операций или -1
     */
    public int MinOperations(int[][] grid, int x) {
        // Разворачиваем в одномерный список
        var flat = new System.Collections.Generic.List<int>();
        foreach (var row in grid)
            foreach (var val in row)
                flat.Add(val);
        
        // Проверка остатков
        int rem = flat[0] % x;
        foreach (int val in flat) {
            if (val % x != rem)
                return -1;
        }
        
        // Сортировка и медиана
        flat.Sort();
        int median = flat[flat.Count / 2];
        
        // Подсчёт операций
        long ops = 0;
        foreach (int val in flat)
            ops += Math.Abs(val - median) / x;
        
        return (int)ops;
    }
}