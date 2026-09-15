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

class Solution {
public:
    vector<long long> distance(vector<int>& nums) {
        int n = nums.size();
        unordered_map<int, vector<int>> mp;
        for (int i = 0; i < n; ++i) {
            mp[nums[i]].push_back(i);
        }
        
        vector<long long> ans(n, 0);
        
        for (auto& [val, indices] : mp) {
            int m = indices.size();
            vector<long long> prefix(m + 1, 0);
            for (int i = 0; i < m; ++i) {
                prefix[i + 1] = prefix[i] + indices[i];
            }
            
            for (int i = 0; i < m; ++i) {
                long long idx = indices[i];
                long long leftCount = i;
                long long leftSum = prefix[i];
                long long leftDist = idx * leftCount - leftSum;
                
                long long rightCount = m - i - 1;
                long long rightSum = prefix[m] - prefix[i + 1];
                long long rightDist = rightSum - idx * rightCount;
                
                ans[idx] = leftDist + rightDist;
            }
        }
        return ans;
    }
};