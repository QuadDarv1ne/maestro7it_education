/**
 * https://leetcode.com/contest/weekly-contest-463/problems/minimum-sum-after-divisible-sum-deletions/
 */

#define LL long long
#define VI vector<int>
#define UMII unordered_map<int, LL>
#define MIN(a, b) ((a) < (b) ? (a) : (b))

class Solution {
public:
    long long minArraySum(vector<int>& nums, int k) {
        UMII min_sum_for_rem;
    min_sum_for_rem[0] = 0;

    LL p_sum = 0;
    LL min_sum = 0;

    for (int num : nums) {
        p_sum += num;
        int rem = (int)((p_sum % k + k) % k);

        LL next_min_sum = min_sum + num;

        if (min_sum_for_rem.count(rem)) {
            next_min_sum = MIN(next_min_sum, min_sum_for_rem[rem]);
        }
        
        min_sum = next_min_sum;

        if (!min_sum_for_rem.count(rem) || min_sum < min_sum_for_rem[rem]) {
            min_sum_for_rem[rem] = min_sum;
        }
    }

    return min_sum;
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