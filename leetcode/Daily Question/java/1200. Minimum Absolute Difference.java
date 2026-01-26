/**
 * Автор: Дуплей Максим Игоревич
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
     * Находит все пары элементов с минимальной абсолютной разностью в массиве.
     * 
     * @param arr массив различных целых чисел.
     * @return список списков пар [a, b], где:
     *         - a < b
     *         - |a - b| минимально среди всех возможных пар
     *         - Пары отсортированы в порядке возрастания внутри каждой пары
     *           и по первому элементу между парами
     * 
     * @note Алгоритм работает за O(n log n) из-за сортировки и использует O(n) памяти.
     * 
     * @example
     *   Solution sol = new Solution();
     *   int[] arr = {4, 2, 1, 3};
     *   List<List<Integer>> result = sol.minimumAbsDifference(arr);
     *   // result = [[1,2],[2,3],[3,4]]
     */
    public List<List<Integer>> minimumAbsDifference(int[] arr) {
        // Сортируем массив для нахождения последовательных элементов с минимальной разностью
        Arrays.sort(arr);
        int minDiff = Integer.MAX_VALUE;
        List<List<Integer>> result = new ArrayList<>();
        
        // Находим минимальную разность
        for (int i = 1; i < arr.length; i++) {
            int diff = arr[i] - arr[i-1];
            if (diff < minDiff) {
                minDiff = diff;
            }
        }
        
        // Собираем пары с минимальной разностью
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] - arr[i-1] == minDiff) {
                List<Integer> pair = new ArrayList<>();
                pair.add(arr[i-1]);
                pair.add(arr[i]);
                result.add(pair);
            }
        }
        
        return result;
    }
}