/**
 * https://leetcode.com/problems/number-of-zero-filled-subarrays/description/?envType=daily-question&envId=2025-08-19
 */

/// <summary>
/// Подсчитывает количество непрерывных подмассивов, состоящих только из нулей.
/// 
/// Идея:
/// Проходим по массиву, храним длину текущего сегмента нулей cnt.
/// При каждом нуле cnt увеличивается и прибавляется к общему ответу.
/// 
/// Время: O(n), Память: O(1)
/// </summary>
public class Solution {
    public long ZeroFilledSubarray(int[] nums) {
        long ans = 0;
        int cnt = 0;
        foreach (int x in nums) {
            if (x == 0) {
                cnt++;
                ans += cnt;
            } else {
                cnt = 0;
            }
        }
        return ans;
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