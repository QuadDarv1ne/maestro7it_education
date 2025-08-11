/**
 * https://leetcode.com/problems/house-robber/description/?envType=study-plan-v2&envId=top-interview-150
 */

class Solution {
    /**
     * Задача: Максимизировать сумму денег, которую можно украсть из домов, не грабя два соседних.
     *
     * @param nums массив с деньгами в каждом доме
     * @return максимальная сумма, которую можно украсть
     *
     * Алгоритм:
     * Используется динамическое программирование:
     * dp[i] = max(dp[i-1], dp[i-2] + nums[i])
     * где dp[i] — максимальная сумма при грабежах домов с 0 по i.
     *
     * Время: O(n), Память: O(n)
     */
    public int rob(int[] nums) {
        if (nums.length == 0) return 0;
        if (nums.length == 1) return nums[0];

        int n = nums.length;
        int[] dp = new int[n];
        dp[0] = nums[0];
        dp[1] = Math.max(nums[0], nums[1]);

        for (int i = 2; i < n; i++) {
            dp[i] = Math.max(dp[i-1], dp[i-2] + nums[i]);
        }
        return dp[n-1];
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