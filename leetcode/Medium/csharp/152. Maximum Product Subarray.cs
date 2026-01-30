/**
 * https://leetcode.com/problems/maximum-product-subarray/description/
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

public class Solution {
    public int MaxProduct(int[] nums) {
        /*
        Находит максимальное произведение подмассива.
        
        Идея:
        - Отслеживаем максимальное и минимальное произведение
        - При встрече отрицательного числа меняем их местами
        */
        
        if (nums == null || nums.Length == 0) {
            return 0;
        }
        
        int maxProd = nums[0];
        int minProd = nums[0];
        int result = nums[0];
        
        for (int i = 1; i < nums.Length; i++) {
            int current = nums[i];
            
            // Если число отрицательное, меняем местами max и min
            if (current < 0) {
                int temp = maxProd;
                maxProd = minProd;
                minProd = temp;
            }
            
            // Обновляем максимальное и минимальное произведение
            maxProd = Math.Max(current, maxProd * current);
            minProd = Math.Min(current, minProd * current);
            
            // Обновляем результат
            result = Math.Max(result, maxProd);
        }
        
        return result;
    }
}