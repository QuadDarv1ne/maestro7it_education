/**
 * https://leetcode.com/problems/sliding-window-maximum/description/
 */

using System.Collections.Generic;

public class Solution {
    public int[] MaxSlidingWindow(int[] nums, int k) {
        LinkedList<int> q = new LinkedList<int>();
        int n = nums.Length;
        int[] ans = new int[n - k + 1];
        int j = 0;
        for (int i = 0; i < n; i++) {
            // Удаляем вышедшие из окна элементы
            if (q.Count > 0 && q.First.Value < i - k + 1)
                q.RemoveFirst();
            // Поддерживаем убывающий порядок
            while (q.Count > 0 && nums[q.Last.Value] <= nums[i])
                q.RemoveLast();
            q.AddLast(i);
            if (i >= k - 1)
                ans[j++] = nums[q.First.Value];
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