/**
 * Решение задачи LeetCode № 3010: "Divide an Array Into Subarrays With Minimum Cost I"
 * https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-i/description/
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
    /**
     * Находит минимальную стоимость разделения массива на 3 подмассива.
     * 
     * Массив делится на 3 непустых подмассива nums[0..i], nums[i+1..j], nums[j+1..n-1].
     * Стоимость = nums[0] + nums[i+1] + nums[j+1] (первые элементы каждого подмассива).
     * 
     * @param nums массив целых чисел
     * @return минимальная стоимость разделения
     */
    public int minimumCost(int[] nums) {
        // nums[0] всегда включается в стоимость
        int cost = nums[0];
        
        // Находим два минимальных элемента среди nums[1:]
        int min1 = Integer.MAX_VALUE, min2 = Integer.MAX_VALUE;
        
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] < min1) {
                min2 = min1;
                min1 = nums[i];
            } else if (nums[i] < min2) {
                min2 = nums[i];
            }
        }
        
        return cost + min1 + min2;
    }
}