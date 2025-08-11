/**
 * https://leetcode.com/problems/gas-station/description/?envType=study-plan-v2&envId=top-interview-150
 */

#include <vector>
using namespace std;

class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        int totalSurplus = 0, currentSurplus = 0, start = 0;
        for (int i = 0; i < gas.size(); ++i) {
            int diff = gas[i] - cost[i];
            totalSurplus += diff;
            currentSurplus += diff;
            if (currentSurplus < 0) {
                start = i + 1;
                currentSurplus = 0;
            }
        }
        return (totalSurplus >= 0) ? start : -1;
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