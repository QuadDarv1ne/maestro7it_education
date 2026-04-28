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

import java.util.*;

class Solution {
    /**
     * Возвращает минимальное количество операций, чтобы все элементы сетки стали равны.
     * За одну операцию можно прибавить x или вычесть x из любого элемента.
     * Если это невозможно, возвращает -1.
     *
     * https://leetcode.com/problems/minimum-operations-to-make-a-uni-value-grid/description/?envType=daily-question&envId=2026-04-28
     * 
     * @param grid двумерный массив целых чисел
     * @param x    целое число, шаг изменения
     * @return минимальное число операций или -1
     */
    public int minOperations(int[][] grid, int x) {
        // Разворачиваем в одномерный список
        List<Integer> flat = new ArrayList<>();
        for (int[] row : grid)
            for (int val : row)
                flat.add(val);
        
        // Проверка остатков
        int rem = flat.get(0) % x;
        for (int val : flat) {
            if (val % x != rem)
                return -1;
        }
        
        // Сортировка и медиана
        Collections.sort(flat);
        int median = flat.get(flat.size() / 2);
        
        // Подсчёт операций (используем long, чтобы избежать переполнения)
        long ops = 0;
        for (int val : flat)
            ops += Math.abs(val - median) / x;
        
        return (int) ops;
    }
}