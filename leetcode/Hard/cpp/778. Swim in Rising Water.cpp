/*
https://leetcode.com/problems/swim-in-rising-water/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

#include <vector>
#include <queue>
#include <tuple>
using namespace std;

class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        vector<vector<bool>> seen(n, vector<bool>(n, false));
        // min-heap: (time, x, y)
        auto cmp = greater<tuple<int,int,int>>();
        priority_queue< tuple<int,int,int>,
                        vector<tuple<int,int,int>>,
                        decltype(cmp) > pq(cmp);

        pq.emplace(grid[0][0], 0, 0);
        seen[0][0] = true;
        int res = 0;
        int dirs[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};

        while (!pq.empty()) {
            auto [time, x, y] = pq.top();
            pq.pop();
            res = max(res, time);
            if (x == n-1 && y == n-1) return res;

            for (auto &d : dirs) {
                int nx = x + d[0], ny = y + d[1];
                if (nx < 0 || nx >= n || ny < 0 || ny >= n) continue;
                if (seen[nx][ny]) continue;
                seen[nx][ny] = true;
                pq.emplace(max(time, grid[nx][ny]), nx, ny);
            }
        }
        return -1;  // теоретически не достижимо
    }
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/