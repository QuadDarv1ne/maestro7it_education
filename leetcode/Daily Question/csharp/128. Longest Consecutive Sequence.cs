public class Solution {
    public int LongestConsecutive(int[] nums) {
        /**
         * Находит длину самой длинной последовательности последовательных чисел.
         * 
         * Алгоритм:
         * 1. Преобразуем массив в множество для быстрого поиска
         * 2. Для каждого числа проверяем, является ли оно началом последовательности
         * 3. Если да, то подсчитываем длину последовательности
         * 
         * Сложность: O(n) время, O(n) память
         *
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
        
        if (nums.Length == 0) {
            return 0;
        }
        
        // Преобразуем массив в множество
        HashSet<int> numSet = new HashSet<int>(nums);
        int maxLength = 0;
        
        foreach (int num in numSet) {
            // Проверяем, является ли число началом последовательности
            if (!numSet.Contains(num - 1)) {
                int currentNum = num;
                int currentLength = 1;
                
                // Подсчитываем длину последовательности
                while (numSet.Contains(currentNum + 1)) {
                    currentNum++;
                    currentLength++;
                }
                
                // Обновляем максимальную длину
                maxLength = Math.Max(maxLength, currentLength);
            }
        }
        
        return maxLength;
    }
}