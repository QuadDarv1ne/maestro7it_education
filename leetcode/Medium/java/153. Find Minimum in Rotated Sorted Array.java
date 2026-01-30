/**
 * https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
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

class Solution {
    public int findMin(int[] nums) {
        /*
        Находит минимальный элемент в повернутом отсортированном массиве.
        
        Идея:
        - Используем бинарный поиск
        - Сравниваем средний элемент с крайним правым
        - Определяем, в какой половине находится минимум
        */
        
        int left = 0;
        int right = nums.length - 1;
        
        // Если массив не повернут или содержит 1 элемент
        if (nums[left] < nums[right] || left == right) {
            return nums[left];
        }
        
        while (left < right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] > nums[right]) {
                // Минимум в правой половине (после mid)
                left = mid + 1;
            } else {
                // Минимум в левой половине (может быть mid)
                right = mid;
            }
        }
        
        return nums[left];
    }
}