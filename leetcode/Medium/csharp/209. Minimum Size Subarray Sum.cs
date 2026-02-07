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
    /**
     * Находит минимальную длину подмассива с суммой >= target
     * 
     * @param target Целевая сумма
     * @param nums Массив положительных целых чисел
     * @return Минимальная длина подмассива или 0
     */
    public int MinSubArrayLen(int target, int[] nums) {
        int n = nums.Length;
        int minLength = int.MaxValue;  // Максимальное значение int
        int currentSum = 0;
        int left = 0;
        
        for (int right = 0; right < n; right++) {
            // Расширяем окно справа
            currentSum += nums[right];
            
            // Сжимаем окно слева, пока сумма >= target
            while (currentSum >= target) {
                // Обновляем минимальную длину
                minLength = Math.Min(minLength, right - left + 1);
                
                // Убираем левый элемент
                currentSum -= nums[left];
                left++;
            }
        }
        
        return minLength == int.MaxValue ? 0 : minLength;
    }
}