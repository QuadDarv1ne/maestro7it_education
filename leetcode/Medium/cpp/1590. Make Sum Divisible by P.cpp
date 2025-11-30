/**
 * https://leetcode.com/problems/make-sum-divisible-by-p/description/?envType=daily-question&envId=2025-11-30
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Make Sum Divisible by P" на C++
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
#include <unordered_map>
using namespace std;

class Solution {
public:
    int minSubarray(vector<int>& nums, int p) {
        long totalSum = 0;
        for (int num : nums) totalSum += num;
        int remainder = totalSum % p;
        if (remainder == 0) return 0;

        unordered_map<int, int> prefixMap;
        prefixMap[0] = -1;
        long prefixSum = 0;
        int minLength = nums.size();

        for (int i = 0; i < nums.size(); ++i) {
            prefixSum = (prefixSum + nums[i]) % p;
            int target = (prefixSum - remainder + p) % p;
            if (prefixMap.find(target) != prefixMap.end()) {
                minLength = min(minLength, i - prefixMap[target]);
            }
            prefixMap[prefixSum] = i;
        }
        return minLength < nums.size() ? minLength : -1;
    }
};