/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /*
     * Для каждого индекса i вычисляет максимальное значение в nums, 
     * которое может быть достигнуто, начиная с i, следуя правилам прыжков.
     */
    vector<int> maxValue(vector<int>& nums) {
        int n = nums.size();
        vector<int> ans(n);

        vector<int> prefix_max(n);
        int cur_max = nums[0];
        for (int i = 0; i < n; ++i) {
            cur_max = max(cur_max, nums[i]);
            prefix_max[i] = cur_max;
        }

        vector<int> suffix_min(n);
        int cur_min = nums.back();
        for (int i = n - 1; i >= 0; --i) {
            cur_min = min(cur_min, nums[i]);
            suffix_min[i] = cur_min;
        }

        vector<int> cut_indices;
        for (int i = 0; i < n - 1; ++i) {
            if (prefix_max[i] <= suffix_min[i + 1]) {
                cut_indices.push_back(i);
            }
        }

        int start = 0;
        for (int cut : cut_indices) {
            int end = cut;
            int seg_max = *max_element(nums.begin() + start, nums.begin() + end + 1);
            for (int i = start; i <= end; ++i) {
                ans[i] = seg_max;
            }
            start = end + 1;
        }

        if (start < n) {
            int seg_max = *max_element(nums.begin() + start, nums.end());
            for (int i = start; i < n; ++i) {
                ans[i] = seg_max;
            }
        }

        return ans;
    }
};