/**
 * https://leetcode.com/contest/weekly-contest-463/problems/best-time-to-buy-and-sell-stock-using-strategy/
 */

#define LL long long
#define FOR(i, a, b) for (int i = (a); i < (b); ++i)
#define MAX(a, b) ((a) > (b) ? (a) : (b))

class Solution {
public:
    long long maxProfit(vector<int>& prices, vector<int>& strategy, int k) {
        int n = prices.size();
    LL initialProfit = 0;
    FOR(i, 0, n) {
        initialProfit += (LL)prices[i] * strategy[i];
    }

    if (k == 0 || k > n) {
        return initialProfit;
    }

    int h = k / 2;
    LL currentGain = 0;

    FOR(i, 0, h) {
        currentGain -= (LL)strategy[i] * prices[i];
    }
    FOR(i, h, k) {
        currentGain += (LL)(1 - strategy[i]) * prices[i];
    }

    LL maxGain = currentGain;

    FOR(i, 1, n - k + 1) {
        currentGain += (LL)strategy[i - 1] * prices[i - 1];
        currentGain -= (LL)prices[i + h - 1];
        currentGain += (LL)(1 - strategy[i + k - 1]) * prices[i + k - 1];
        maxGain = MAX(maxGain, currentGain);
    }

    return initialProfit + MAX(0LL, maxGain);
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