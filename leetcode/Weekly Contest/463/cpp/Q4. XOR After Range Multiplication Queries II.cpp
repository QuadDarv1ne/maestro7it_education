/**
 * https://leetcode.com/contest/weekly-contest-463/problems/xor-after-range-multiplication-queries-ii/
 */

#define LL long long
#define VECI vector<int>
#define VECVI vector<vector<int>>
#define MOD 1000000007

class Solution {
public:
    LL power(LL base, LL exp) {
    LL res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}

LL modInverse(LL n) {
    return power(n, MOD - 2);
}

int xorAfterQueries(VECI& nums, VECVI& queries) {
    int n = nums.size();
    int B = 450; 

    vector<VECI> queries_by_k[B + 1];

    for (const auto& q : queries) {
        int k = q[2];
        if (k > B) {
            int l = q[0], r = q[1], v = q[3];
            for (int i = l; i <= r; i += k) {
                nums[i] = (int)(((LL)nums[i] * v) % MOD);
            }
        } else {
            queries_by_k[k].push_back(q);
        }
    }

    for (int k = 1; k <= B; ++k) {
        if (queries_by_k[k].empty()) {
            continue;
        }

        VECVI diffs(k);
        for(int rem = 0; rem < k; ++rem) {
            int prog_len = (n > rem) ? (n - 1 - rem) / k + 1 : 0;
            if (prog_len > 0) {
                diffs[rem].assign(prog_len + 1, 1);
            }
        }

        for (const auto& q : queries_by_k[k]) {
            int l = q[0], r = q[1], v = q[3];
            int rem = l % k;

            if (diffs[rem].empty()) continue;

            int start_idx = (l - rem) / k;
            int r_prime = r - (r - rem + k) % k;
            int end_idx = (r_prime - rem) / k;

            diffs[rem][start_idx] = (int)(((LL)diffs[rem][start_idx] * v) % MOD);
            if (end_idx + 1 < diffs[rem].size()) {
                LL inv_v = modInverse(v);
                diffs[rem][end_idx + 1] = (int)(((LL)diffs[rem][end_idx + 1] * inv_v) % MOD);
            }
        }

        for (int rem = 0; rem < k; ++rem) {
            if (diffs[rem].empty()) continue;

            LL current_mult = 1;
            for (int j = 0; j < diffs[rem].size() - 1; ++j) {
                current_mult = (current_mult * diffs[rem][j]) % MOD;
                if (current_mult != 1) {
                    int original_idx = rem + j * k;
                    nums[original_idx] = (int)(((LL)nums[original_idx] * current_mult) % MOD);
                }
            }
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