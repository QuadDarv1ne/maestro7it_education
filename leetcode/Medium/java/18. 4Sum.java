/**
 * https://leetcode.com/problems/4sum/description/
 */

import java.util.*;

class Solution {
    /**
     * Описание:
     *   Находит все уникальные четвёрки чисел из массива nums, сумма которых равна target.
     *
     * Параметры:
     *   nums - массив целых чисел
     *   target - целевая сумма
     *
     * Возвращает:
     *   Список уникальных квартетов в произвольном порядке.
     *
     * Идея алгоритма:
     *   Сортировка + два внешних индекса (i, j) и два указателя (l, r) внутри.
     *   Дубликаты пропускаются на всех уровнях.
     *
     * Сложность:
     *   Время O(n^3), Память O(1) дополнительная.
     */
    public List<List<Integer>> fourSum(int[] nums, int target) {
        Arrays.sort(nums);
        int n = nums.length;
        List<List<Integer>> res = new ArrayList<>();

        for (int i = 0; i < n - 3; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            for (int j = i + 1; j < n - 2; j++) {
                if (j > i + 1 && nums[j] == nums[j - 1]) continue;

                int l = j + 1, r = n - 1;
                while (l < r) {
                    long sum = 0L + nums[i] + nums[j] + nums[l] + nums[r]; // избегаем переполнения
                    if (sum == target) {
                        res.add(Arrays.asList(nums[i], nums[j], nums[l], nums[r]));
                        l++; r--;
                        while (l < r && nums[l] == nums[l - 1]) l++;
                        while (l < r && nums[r] == nums[r + 1]) r--;
                    } else if (sum < target) {
                        l++;
                    } else {
                        r--;
                    }
                }
            }
        }
        return res;
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