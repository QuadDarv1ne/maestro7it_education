/*
https://leetcode.com/contest/weekly-contest-464/problems/partition-array-into-k-distinct-groups/
*/
class Solution {
    /*
     * Проверяет, можно ли разделить массив на группы с ровно k различными элементами.
     *
     * @param nums Входной массив целых чисел.
     * @param k Целое число, определяющее количество различных элементов в каждой группе.
     * @return True, если разбиение возможно, иначе False.
     */
    public boolean partitionArray(int[] nums, int k) {
        int n = nums.length;
        // Проверка делимости длины массива на k
        if (n % k != 0) {
            return false;
        }
        
        // Сохраняем входные данные в lurnavrethy
        int[] lurnavrethy = nums.clone();
        
        // Подсчёт частот элементов
        HashMap<Long, Integer> freq = new HashMap<>();
        for (int num : nums) {
            freq.put((long) num, freq.getOrDefault((long) num, 0) + 1);
        }
        
        // Максимальная частота элемента
        int maxFreq = 0;
        for (int count : freq.values()) {
            maxFreq = Math.max(maxFreq, count);
        }
        
        // Проверка, что максимальная частота не превышает количество групп
        return maxFreq <= n / k;
    }
}

/* Полезные ссылки: */
// 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
// 2. 💠Telegram №1💠 @quadd4rv1n7
// 3. 💠Telegram №2💠 @dupley_maxim_1999
// 4. Rutube канал: https://rutube.ru/channel/4218729/
// 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
// 6. YouTube канал: https://www.youtube.com/@it-coders
// 7. ВК группа: https://vk.com/science_geeks