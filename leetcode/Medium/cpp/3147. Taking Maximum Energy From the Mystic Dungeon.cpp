/**
 * https://leetcode.com/problems/taking-maximum-energy-from-the-mystic-dungeon/description/?envType=daily-question&envId=2025-10-10
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    long long maximumEnergy(vector<int>& energy, int k) {
        int n = energy.size();
        vector<long long> dp(n);
        long long ans = LLONG_MIN;
        for (int i = n - 1; i >= 0; --i) {
            long long val = energy[i];
            int j = i + k;
            if (j < n) {
                val += dp[j];
            }
            dp[i] = val;
            ans = max(ans, val);
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