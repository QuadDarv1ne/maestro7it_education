/**
 * https://leetcode.com/problems/sliding-window-maximum/description/
 */

import java.util.*;

class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        Deque<Integer> q = new ArrayDeque<>();
        int n = nums.length;
        int[] ans = new int[n - k + 1];
        for (int i = 0, j = 0; i < n; ++i) {
            // Удаляем индексы вне окна
            if (!q.isEmpty() && q.peekFirst() < i - k + 1)
                q.pollFirst();
            // Удаляем элементы с меньшими значениями
            while (!q.isEmpty() && nums[q.peekLast()] <= nums[i])
                q.pollLast();
            q.offerLast(i);
            // Добавляем максимум текущего окна
            if (i >= k - 1)
                ans[j++] = nums[q.peekFirst()];
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