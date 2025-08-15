/**
 * https://leetcode.com/problems/top-k-frequent-elements/
 */

class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int,int> cnt;
        for (int x : nums) cnt[x]++;
        vector<vector<int>> buckets(nums.size() + 1);
        for (auto& [num, f] : cnt) {
            buckets[f].push_back(num);
        }
        vector<int> res;
        for (int i = buckets.size() - 1; i >= 0 && res.size() < k; --i) {
            for (int num : buckets[i]) {
                res.push_back(num);
                if (res.size() == k) break;
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