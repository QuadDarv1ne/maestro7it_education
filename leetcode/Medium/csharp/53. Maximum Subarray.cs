/**
 * https://leetcode.com/problems/maximum-subarray/description/?envType=study-plan-v2&envId=top-interview-150
 */

public class Solution {
    /// <summary>
    /// Метод находит максимальную сумму подмассива в заданном массиве целых чисел.
    /// </summary>
    /// <param name="nums">Массив целых чисел</param>
    /// <returns>Максимальная сумма подмассива</returns>
    public int MaxSubArray(int[] nums) {
        int currentSum = nums[0];
        int maxSum = nums[0];

        for (int i = 1; i < nums.Length; i++) {
            // Обновляем текущую сумму: либо начинаем новый подмассив с nums[i], либо продолжаем текущий
            currentSum = Math.Max(nums[i], currentSum + nums[i]);

            // Обновляем максимум
            maxSum = Math.Max(maxSum, currentSum);
        }

        return maxSum;
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