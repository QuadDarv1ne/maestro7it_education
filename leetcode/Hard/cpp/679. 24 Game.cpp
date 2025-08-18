/**
 * https://leetcode.com/problems/24-game/description/
 */

#include <vector>
#include <cmath>
using namespace std;

class Solution {
public:
    bool judgePoint24(vector<int>& cards) {
        vector<double> nums(cards.begin(), cards.end());
        return dfs(nums);
    }

private:
    bool dfs(vector<double>& nums) {
        const double EPS = 1e-6;
        int n = nums.size();
        if (n == 1) return fabs(nums[0] - 24.0) < EPS;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                double a = nums[i], b = nums[j];
                vector<double> rest;
                for (int k = 0; k < n; k++) {
                    if (k != i && k != j) rest.push_back(nums[k]);
                }
                vector<double> results = {a + b, a - b, b - a, a * b};
                if (fabs(b) > EPS) results.push_back(a / b);
                if (fabs(a) > EPS) results.push_back(b / a);
                for (double r : results) {
                    rest.push_back(r);
                    if (dfs(rest)) return true;
                    rest.pop_back();
                }
            }
        }
        return false;
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