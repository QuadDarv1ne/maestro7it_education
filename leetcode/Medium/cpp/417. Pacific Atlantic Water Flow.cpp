/*
https://leetcode.com/problems/pacific-atlantic-water-flow/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

#include <vector>
using namespace std;

class Solution {
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        int m = heights.size(), n = heights[0].size();
        vector<vector<int>> res;
        vector<vector<bool>> pac(m, vector<bool>(n, false));
        vector<vector<bool>> atl(m, vector<bool>(n, false));
        vector<pair<int,int>> dirs = {{1,0},{-1,0},{0,1},{0,-1}};

        auto dfs = [&](auto&& self, int x, int y, vector<vector<bool>>& visited) -> void {
            visited[x][y] = true;
            for (auto& [dx, dy] : dirs) {
                int nx = x + dx, ny = y + dy;
                if (nx >= 0 && nx < m && ny >= 0 && ny < n && !visited[nx][ny] && heights[nx][ny] >= heights[x][y])
                    self(self, nx, ny, visited);
            }
        };

        for (int i = 0; i < m; i++) {
            dfs(dfs, i, 0, pac);
            dfs(dfs, i, n - 1, atl);
        }
        for (int j = 0; j < n; j++) {
            dfs(dfs, 0, j, pac);
            dfs(dfs, m - 1, j, atl);
        }

        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (pac[i][j] && atl[i][j]) res.push_back({i, j});
        return res;
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