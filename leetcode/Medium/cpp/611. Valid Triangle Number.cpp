/**
 * https://leetcode.com/problems/valid-triangle-number/description/?envType=daily-question&envId=2025-09-26
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int triangleNumber(vector<int>& nums) {
        /*
        Возвращает количество троек (i, j, k), которые могут образовать треугольник.
        
        Алгоритм:
        1. Сортируем массив.
        2. Фиксируем nums[k] как наибольшую сторону.
        3. Используем два указателя l и r для подсчёта всех возможных пар.
        */
        sort(nums.begin(), nums.end());
        int n = nums.size();
        int ans = 0;
        for (int k = n - 1; k >= 2; --k) {
            int l = 0, r = k - 1;
            while (l < r) {
                if (nums[l] + nums[r] > nums[k]) {
                    ans += (r - l);
                    --r;
                } else {
                    ++l;
                }
            }
        }
        return ans;
    }
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/