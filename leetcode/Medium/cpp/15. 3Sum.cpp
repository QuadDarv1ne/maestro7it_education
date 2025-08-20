/**
 * https://leetcode.com/problems/3sum/description/
 */

#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    /**
     * Найти все уникальные тройки nums[i] + nums[j] + nums[k] == 0.
     *
     * Метод:
     *  - Сортировка массива.
     *  - Для каждого i используем два указателя l и r для поиска пар.
     *  - Пропускаем дубликаты, чтобы не было одинаковых троек.
     *
     * Время: O(n^2), Память: O(1) (кроме результата).
     */
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;
        int n = (int)nums.size();
        for (int i = 0; i < n - 2; ++i) {
            if (i > 0 && nums[i] == nums[i - 1]) continue; // пропустить дубль
            if (nums[i] > 0) break; // дальше суммы будут > 0
            int l = i + 1, r = n - 1;
            while (l < r) {
                long long s = (long long)nums[i] + nums[l] + nums[r];
                if (s < 0) ++l;
                else if (s > 0) --r;
                else {
                    res.push_back({nums[i], nums[l], nums[r]});
                    while (l < r && nums[l] == nums[l + 1]) ++l;
                    while (l < r && nums[r] == nums[r - 1]) --r;
                    ++l; --r;
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