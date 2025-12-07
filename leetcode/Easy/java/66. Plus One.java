class Solution {
    public int[] plusOne(int[] digits) {
        /**
         * Автор: Дуплей Максим Игоревич
         * ORCID: https://orcid.org/0009-0007-7605-539X
         * GitHub: https://github.com/QuadDarv1ne/
         * 
         * Задача: Plus One (LeetCode)
         * Алгоритм: Симуляция сложения с переносом разряда
         * Сложность: O(n) по времени, O(1) по памяти (O(n) в худшем случае)
         * 
         * Идея решения:
         * 1. Идем с конца массива (младший разряд)
         * 2. Если цифра < 9, увеличиваем на 1 и возвращаем
         * 3. Если цифра = 9, ставим 0 и переносим 1 дальше
         * 4. Если все цифры были 9, создаем новый массив с 1 в начале
         */
        
        int n = digits.length;
        
        // Идем с конца массива
        for (int i = n - 1; i >= 0; i--) {
            // Если текущая цифра меньше 9
            if (digits[i] < 9) {
                digits[i]++;
                return digits; // Готово, переноса нет
            }
            // Если цифра = 9, ставим 0 и идем дальше (перенос)
            digits[i] = 0;
        }
        
        // Если дошли сюда, значит все цифры были 9
        // Например: [9,9,9] -> [1,0,0,0]
        int[] result = new int[n + 1];
        result[0] = 1;
        return result;
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