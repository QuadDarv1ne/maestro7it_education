/**
 * https://leetcode.com/problems/24-game/description/
 */
using System;
using System.Collections.Generic;

public class Solution {
    /**
     * Определяет, можно ли из четырех карт составить выражение, равное 24,
     * используя операции +, -, *, / и скобки.
     */
    public bool JudgePoint24(int[] cards) {
        var nums = new List<double>();
        foreach (var c in cards) nums.Add(c);
        return Dfs(nums);
    }

    private bool Dfs(List<double> nums) {
        const double EPS = 1e-6;
        if (nums.Count == 1) {
            return Math.Abs(nums[0] - 24.0) < EPS;
        }
        int n = nums.Count;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                double a = nums[i], b = nums[j];
                var rest = new List<double>();
                for (int k = 0; k < n; k++) {
                    if (k != i && k != j) rest.Add(nums[k]);
                }
                var results = new List<double> { a + b, a - b, b - a, a * b };
                if (Math.Abs(b) > EPS) results.Add(a / b);
                if (Math.Abs(a) > EPS) results.Add(b / a);

                foreach (var r in results) {
                    rest.Add(r);
                    if (Dfs(rest)) return true;
                    rest.RemoveAt(rest.Count - 1);
                }
            }
        }
        return false;
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