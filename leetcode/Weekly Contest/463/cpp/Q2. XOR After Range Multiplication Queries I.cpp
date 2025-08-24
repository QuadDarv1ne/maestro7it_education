/**
 * https://leetcode.com/contest/weekly-contest-463/problems/xor-after-range-multiplication-queries-i/
 */

#define LL long long
#define VECI vector<int>
#define VECVI vector<vector<int>>
#define MOD 1000000007
#define FOR_EACH_Q(q, queries) for (const auto& q : queries)
#define FOR_STEP(i, l, r, k) for (int i = (l); i <= (r); i += (k))

class Solution {
public:
    int xorAfterQueries(vector<int>& nums, vector<vector<int>>& queries) {
        FOR_EACH_Q(q, queries) {
        int l = q[0];
        int r = q[1];
        int k = q[2];
        int v = q[3];
        FOR_STEP(idx, l, r, k) {
            nums[idx] = (int)(((LL)nums[idx] * v) % MOD);
        }
    }

    int xorSum = 0;
    for (int num : nums) {
        xorSum ^= num;
    }

    return xorSum;
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