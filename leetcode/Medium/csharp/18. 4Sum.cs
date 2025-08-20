/**
 * https://leetcode.com/problems/4sum/description/
 */

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Описание:
    ///   Находит все уникальные четвёрки чисел из массива nums с суммой target.
    ///
    /// Параметры:
    ///   nums: массив целых чисел
    ///   target: целевая сумма
    ///
    /// Возвращает:
    ///   Список списков (четвёрок) без дубликатов.
    ///
    /// Идея алгоритма:
    ///   Сортировка; двойной цикл по i, j; внутри два указателя l/r.
    ///   Дубликаты пропускаются на всех этапах.
    ///
    /// Сложность:
    ///   Время O(n^3), Память O(1) доп.
    /// </summary>
    public IList<IList<int>> FourSum(int[] nums, int target) {
        Array.Sort(nums);
        int n = nums.Length;
        var res = new List<IList<int>>();

        for (int i = 0; i < n - 3; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            for (int j = i + 1; j < n - 2; j++) {
                if (j > i + 1 && nums[j] == nums[j - 1]) continue;

                int l = j + 1, r = n - 1;
                while (l < r) {
                    long sum = (long)nums[i] + nums[j] + nums[l] + nums[r]; // предотвращаем переполнение
                    if (sum == target) {
                        res.Add(new List<int> { nums[i], nums[j], nums[l], nums[r] });
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