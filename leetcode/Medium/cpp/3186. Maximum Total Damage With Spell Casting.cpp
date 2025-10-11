/**
 * https://leetcode.com/problems/maximum-total-damage-with-spell-casting/?envType=daily-question&envId=2025-10-11
 */

#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    long long maximumTotalDamage(vector<int>& power) {
        unordered_map<int, int> cnt;
        for (int p : power) cnt[p]++;
        vector<int> uniq;
        uniq.reserve(cnt.size());
        for (auto& [v, _] : cnt) uniq.push_back(v);
        sort(uniq.begin(), uniq.end());
        int n = uniq.size();

        vector<int> nxt(n);
        for (int i = 0; i < n; ++i) {
            int j = upper_bound(uniq.begin(), uniq.end(), uniq[i] + 2) - uniq.begin();
            nxt[i] = j;
        }

        vector<long long> dp(n + 1, 0);
        for (int i = n - 1; i >= 0; --i) {
            long long skip = dp[i + 1];
            long long take = 1LL * uniq[i] * cnt[uniq[i]] + dp[nxt[i]];
            dp[i] = max(skip, take);
        }

        return dp[0];
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