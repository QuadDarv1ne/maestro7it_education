/**
 * https://leetcode.com/problems/maximum-sum-circular-subarray/description/?envType=study-plan-v2&envId=top-interview-150
 */

public class Solution {
    /// <summary>
    /// Метод возвращает максимальную сумму подмассива в кольцевом массиве.
    /// Кольцевой массив — это массив, где конец соединён с началом,
    /// поэтому подмассив может перекрываться через границу массива.
    /// </summary>
    /// <param name="nums">Входной массив целых чисел.</param>
    /// <returns>Максимальная сумма подмассива с учётом кольцевой структуры.</returns>
    public int MaxSubarraySumCircular(int[] nums) {
        int totalSum = 0;
        foreach (int num in nums) totalSum += num;
        
        int maxSum = Kadane(nums, false);
        int minSum = Kadane(nums, true);

        // Если все числа отрицательные, возвращаем максимальное значение
        if (totalSum == minSum)
            return maxSum;

        return Math.Max(maxSum, totalSum - minSum);
    }

    /// <summary>
    /// Вспомогательный метод алгоритма Кадане.
    /// Если findMin == false — ищет максимальную сумму подмассива.
    /// Если findMin == true — ищет минимальную сумму подмассива.
    /// </summary>
    /// <param name="nums">Входной массив целых чисел.</param>
    /// <param name="findMin">Флаг поиска минимальной суммы.</param>
    /// <returns>Максимальная или минимальная сумма подмассива.</returns>
    private int Kadane(int[] nums, bool findMin) {
        int currSum = nums[0];
        int result = nums[0];
        for (int i = 1; i < nums.Length; i++) {
            if (findMin) {
                currSum = Math.Min(nums[i], currSum + nums[i]);
                result = Math.Min(result, currSum);
            } else {
                currSum = Math.Max(nums[i], currSum + nums[i]);
                result = Math.Max(result, currSum);
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