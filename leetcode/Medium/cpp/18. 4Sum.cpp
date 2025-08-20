/**
 * https://leetcode.com/problems/4sum/description/
 */

#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    /**
     * Описание:
     *   Возвращает все уникальные четвёрки чисел из nums с суммой target.
     *
     * Параметры:
     *   nums - вектор целых чисел
     *   target - целевая сумма
     *
     * Возвращает:
     *   Вектор уникальных квартетов (каждый как vector<int> из 4 элементов).
     *
     * Идея:
     *   Сортировка, двойной цикл по i и j, внутри два указателя l/r.
     *   Аккуратно пропускаем дубликаты.
     *
     * Сложность:
     *   Время O(n^3), Память O(1) доп.
     */
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        int n = (int)nums.size();
        vector<vector<int>> res;

        for (int i = 0; i < n - 3; ++i) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            for (int j = i + 1; j < n - 2; ++j) {
                if (j > i + 1 && nums[j] == nums[j - 1]) continue;

                int l = j + 1, r = n - 1;
                while (l < r) {
                    long long sum = (long long)nums[i] + nums[j] + nums[l] + nums[r];
                    if (sum == target) {
                        res.push_back({nums[i], nums[j], nums[l], nums[r]});
                        ++l; --r;
                        while (l < r && nums[l] == nums[l - 1]) ++l;
                        while (l < r && nums[r] == nums[r + 1]) --r;
                    } else if (sum < target) {
                        ++l;
                    } else {
                        --r;
                    }
                }
            }
        }
        return res;
    }
};

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