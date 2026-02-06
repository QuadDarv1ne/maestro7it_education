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
     * Находит два числа в отсортированном массиве, сумма которых равна target.
     * Возвращает 1-индексированные позиции этих чисел.
     * 
     * Сложность по времени: O(n)
     * Сложность по памяти: O(1)
     */
    public int[] TwoSum(int[] numbers, int target) {
        int left = 0;
        int right = numbers.Length - 1;
        
        while (left < right) {
            int currentSum = numbers[left] + numbers[right];
            
            if (currentSum == target) {
                // Возвращаем 1-индексированные позиции
                return new int[] { left + 1, right + 1 };
            } else if (currentSum < target) {
                // Нужна большая сумма - сдвигаем left вправо
                left++;
            } else {
                // Нужна меньшая сумма - сдвигаем right влево
                right--;
            }
        }
        
        return new int[] { -1, -1 };
    }
}