public class Solution {
    /**
     * Вычисляет максимальную сумму счастья выбранных детей.
     * 
     * @param happiness массив значений счастья
     * @param k количество детей для выбора
     * @return максимальная сумма счастья
     * 
     * Автор: Дуплей Максим Игоревич
     * ORCID: https://orcid.org/0009-0007-7605-539X
     * GitHub: https://github.com/QuadDarv1ne/
     */
    public long MaximumHappinessSum(int[] happiness, int k) {
        // Сортируем по убыванию
        Array.Sort(happiness);
        Array.Reverse(happiness);
        
        // Суммируем первые k элементов с учетом уменьшения
        long total = 0;
        for (int i = 0; i < k; i++) {
            // Текущее счастье после i уменьшений
            long current = Math.Max(0, (long)happiness[i] - i);
            total += current;
        }
        
        return total;
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/