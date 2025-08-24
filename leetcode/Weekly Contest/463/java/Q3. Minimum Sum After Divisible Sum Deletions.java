/**
 * https://leetcode.com/contest/weekly-contest-463/problems/minimum-sum-after-divisible-sum-deletions/
 */

class Solution {
    public long minArraySum(int[] nums, int k) {
        long dp[] = new long[k], sum = 0, max = 0;
        for (int i = 1; i < k; i++) {
            dp[i] = Long.MIN_VALUE;
        }
        for (int num : nums) {
            sum += num;
            max = Math.max(max, dp[(int) (sum % k)] + sum);
            dp[(int) (sum % k)] = Math.max(dp[(int) (sum % k)], max - sum);
        }
        return sum - max;
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