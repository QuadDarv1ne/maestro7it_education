/**
 * https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/
 */

/// <summary>
/// Удаляет дубликаты из отсортированного массива.
/// Метод двух указателей: i (медленный) и j (быстрый).
/// Время: O(n), Память: O(1)
/// </summary>
public class Solution {
    public int RemoveDuplicates(int[] nums) {
        if (nums == null || nums.Length == 0) return 0;
        int i = 0;
        for (int j = 1; j < nums.Length; j++) {
            if (nums[j] != nums[i]) {
                i++;
                nums[i] = nums[j];
            }
        }
        return i + 1;
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