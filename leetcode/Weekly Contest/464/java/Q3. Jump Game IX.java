/*
https://leetcode.com/contest/weekly-contest-464/problems/jump-game-ix/
*/

class Solution {
    public int[] maxValue(int[] nums) {
        int pref[] = new int[nums.length + 1], suff[] = new int[nums.length + 1], result[] = new int[nums.length], index = 0, max = 0;
        for (int i = 0; i <= nums.length; i++) {
            suff[i] = Integer.MAX_VALUE;
        }
        for (int i = 0; i < nums.length; i++) {
            pref[i + 1] = Math.max(pref[i], nums[i]);
        }
        for (int i = nums.length - 1; i >= 0; i--) {
            suff[i] = Math.min(suff[i + 1], nums[i]);
        }
        for (int i = 0; i < nums.length - 1; i++) {
            max = Math.max(max, nums[i]);
            if (pref[i + 1] <= suff[i + 1]) {
                for (int j = index; j <= i; j++) {
                    result[j] = max;
                }
                max = nums[index = i + 1];
            }
        }
        for (int i = index; i < nums.length; i++) {
            max = Math.max(max, nums[i]);
        }
        for (int i = index; i < nums.length; i++) {
            result[i] = max;
        }
        return result;
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