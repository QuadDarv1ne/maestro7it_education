/**
 * https://leetcode.com/problems/maximum-sum-circular-subarray/description/?envType=study-plan-v2&envId=top-interview-150
 */

/**
 * Класс Solution содержит метод для нахождения максимальной суммы подмассива
 * в кольцевом массиве целых чисел.
 */
class Solution {
    /**
     * Метод возвращает максимальную сумму подмассива в кольцевом массиве.
     * Кольцевой массив — это массив, где конец соединён с началом,
     * поэтому подмассив может перекрываться через границу массива.
     *
     * @param nums Входной массив целых чисел.
     * @return Максимальная сумма подмассива с учётом кольцевой структуры.
     */
    public int maxSubarraySumCircular(int[] nums) {
        int totalSum = 0;
        for (int num : nums) totalSum += num;

        int maxSum = kadane(nums, false);
        int minSum = kadane(nums, true);

        // Если все числа отрицательные, возвращаем максимальное значение
        if (totalSum == minSum)
            return maxSum;

        return Math.max(maxSum, totalSum - minSum);
    }

    /**
     * Вспомогательный метод алгоритма Кадане.
     * Если findMin == false — ищет максимальную сумму подмассива.
     * Если findMin == true — ищет минимальную сумму подмассива.
     *
     * @param nums Входной массив целых чисел.
     * @param findMin Флаг поиска минимальной суммы.
     * @return Максимальная или минимальная сумма подмассива.
     */
    private int kadane(int[] nums, boolean findMin) {
        int currSum = nums[0];
        int result = nums[0];
        for (int i = 1; i < nums.length; i++) {
            if (findMin) {
                currSum = Math.min(nums[i], currSum + nums[i]);
                result = Math.min(result, currSum);
            } else {
                currSum = Math.max(nums[i], currSum + nums[i]);
                result = Math.max(result, currSum);
            }
        }
        return result;
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/