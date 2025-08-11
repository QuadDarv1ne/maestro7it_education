/**
 * https://leetcode.com/problems/house-robber/description/?envType=study-plan-v2&envId=top-interview-150
 */

public class Solution {
    /// <summary>
    /// Задача: максимизировать сумму украденных денег, грабя дома в ряд,
    /// при условии, что нельзя грабить два соседних дома.
    /// </summary>
    /// <param name="nums">Массив с деньгами в домах</param>
    /// <returns>Максимальная сумма, которую можно украсть</returns>
    /// <remarks>
    /// Используется динамическое программирование:
    /// dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    /// Время: O(n), Память: O(n)
    /// </remarks>
    public int Rob(int[] nums) {
        if (nums.Length == 0) return 0;
        if (nums.Length == 1) return nums[0];

        int n = nums.Length;
        int[] dp = new int[n];
        dp[0] = nums[0];
        dp[1] = Math.Max(nums[0], nums[1]);

        for (int i = 2; i < n; i++) {
            dp[i] = Math.Max(dp[i - 1], dp[i - 2] + nums[i]);
        }

        return dp[n - 1];
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