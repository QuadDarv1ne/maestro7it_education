/*
 * https://leetcode.com/problems/maximum-subarray-sum-with-length-divisible-by-k/description/?envType=daily-question&envId=2025-11-27
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 */

class Solution {
public:
    long long maxSubarraySum(vector<int>& nums, int k) {
        int n = nums.size();
        vector<long long> prefix(n + 1, 0);
        
        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
        
        long long maxSum = LLONG_MIN;
        unordered_map<int, long long> minPrefix;
        minPrefix[0] = 0;
        
        for (int i = 1; i <= n; i++) {
            int remainder = i % k;
            
            if (minPrefix.find(remainder) != minPrefix.end()) {
                long long currentSum = prefix[i] - minPrefix[remainder];
                maxSum = max(maxSum, currentSum);
            }
            
            if (minPrefix.find(remainder) == minPrefix.end()) {
                minPrefix[remainder] = prefix[i];
            } else {
                minPrefix[remainder] = min(minPrefix[remainder], prefix[i]);
            }
        }
        
        return maxSum == LLONG_MIN ? 0 : maxSum;
    }
};

/*
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
*/