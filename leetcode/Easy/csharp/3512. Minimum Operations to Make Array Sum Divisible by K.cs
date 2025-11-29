public class Solution {
    public int MinOperations(int[] nums, int k) {
        /**
         * Автор: Дуплей Максим Игоревич
         * ORCID: https://orcid.org/0009-0007-7605-539X
         * GitHub: https://github.com/QuadDarv1ne/
         * 
         * Алгоритм:
         * 1. Вычисляем общую сумму массива
         * 2. Находим остаток от деления суммы на k
         * 3. Если остаток равен 0, операций не требуется
         * 4. Иначе возвращаем остаток как количество операций
         * 
         * Сложность: O(n) по времени, O(1) по памяти
         */
        
        long totalSum = 0;
        foreach(int num in nums) {
            totalSum += num;
        }
        
        return (int)(totalSum % k);
    }
}

/*
 * Полезные ссылки автора:
 * Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * Telegram: @quadd4rv1n7, @dupley_maxim_1999
 * Rutube: https://rutube.ru/channel/4218729/
 * Plvideo: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * YouTube: https://www.youtube.com/@it-coders
 * VK: https://vk.com/science_geeks
 */