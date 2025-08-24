/**
 * https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/description/?envType=daily-question&envId=2025-08-24
 */

public class Solution {
    /// <summary>
    /// Задача: Найти длину самой длинной последовательности из единиц,
    /// если можно удалить ровно один элемент массива.
    ///
    /// Метод:
    /// - Используем скользящее окно.
    /// - Разрешаем максимум один ноль внутри окна.
    /// - Если нулей больше одного → двигаем левую границу.
    /// - Ответ = максимум (right - left).
    ///
    /// Сложность:
    /// - Время: O(n)
    /// - Память: O(1)
    /// </summary>
    public int LongestSubarray(int[] nums) {
        int ans = 0, zeros = 0, left = 0;
        for (int right = 0; right < nums.Length; right++) {
            if (nums[right] == 0) zeros++;
            while (zeros > 1) {
                if (nums[left] == 0) zeros--;
                left++;
            }
            ans = Math.Max(ans, right - left);
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