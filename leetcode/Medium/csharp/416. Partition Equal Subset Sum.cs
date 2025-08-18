/**
 * https://leetcode.com/problems/partition-equal-subset-sum/description/
 */
public class Solution {
    /**
     * Определяет, можно ли разделить массив nums на два подмножества с одинаковой суммой.
     *
     * @param nums массив чисел
     * @return true, если можно разделить, иначе false
     */
    public bool CanPartition(int[] nums) {
        int totalSum = 0;
        foreach (int num in nums) totalSum += num;

        if (totalSum % 2 != 0) return false;

        int target = totalSum / 2;
        bool[] dp = new bool[target + 1];
        dp[0] = true;

        foreach (int num in nums) {
            for (int i = target; i >= num; i--) {
                dp[i] = dp[i] || dp[i - num];
            }
        }

        return dp[target];
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