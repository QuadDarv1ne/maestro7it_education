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

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    long long maximumScore(vector<vector<int>>& grid) {
        const int n = grid.size();
        // prefix[j][i] = сумма первых i элементов в столбце j
        vector<vector<long long>> prefix(n, vector<long long>(n + 1, 0));
        for (int j = 0; j < n; ++j) {
            for (int i = 0; i < n; ++i) {
                prefix[j][i + 1] = prefix[j][i] + grid[i][j];
            }
        }

        // prevPick[i] = максимальный счет до предыдущего столбца при высоте i
        // prevSkip[i] = максимальный счет до столбца перед предыдущим при высоте i
        vector<long long> prevPick(n + 1, 0);
        vector<long long> prevSkip(n + 1, 0);

        for (int j = 1; j < n; ++j) {
            vector<long long> currPick(n + 1, 0);
            vector<long long> currSkip(n + 1, 0);

            for (int curr = 0; curr <= n; ++curr) {
                for (int prev = 0; prev <= n; ++prev) {
                    if (curr > prev) {
                        long long score = prefix[j - 1][curr] - prefix[j - 1][prev];
                        currPick[curr] = max(currPick[curr], prevSkip[prev] + score);
                        currSkip[curr] = max(currSkip[curr], prevSkip[prev] + score);
                    } else {
                        long long score = prefix[j][prev] - prefix[j][curr];
                        currPick[curr] = max(currPick[curr], prevPick[prev] + score);
                        currSkip[curr] = max(currSkip[curr], prevPick[prev]);
                    }
                }
            }
            prevPick = move(currPick);
            prevSkip = move(currSkip);
        }

        return *max_element(prevPick.begin(), prevPick.end());
    }
};