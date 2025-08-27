/**
 * https://leetcode.com/problems/length-of-longest-v-shaped-diagonal-segment/description/?envType=daily-question&envId=2025-08-27
 */

class Solution {
public:
    /**
     * Задача:
     * В матрице grid нужно найти длину самого длинного "V-образного"
     * диагонального сегмента.
     *
     * Правила сегмента:
     * 1. Сегмент начинается с числа 1.
     * 2. Далее значения чередуются по шаблону 2,0,2,0,...
     * 3. Разрешён один поворот на 90° по часовой стрелке.
     */
    int lenOfVDiagonal(vector<vector<int>>& grid) {
        int n = grid.size(), m = grid[0].size();
        vector<vector<vector<int>>> end(4, vector<vector<int>>(n, vector<int>(m, 0)));
        vector<vector<vector<int>>> go(4, vector<vector<int>>(n, vector<int>(m, 1)));

        auto ok = [&](int a, int b) {
            if (a == 1) return b == 2;
            if (a == 2) return b == 0;
            if (a == 0) return b == 2;
            return false;
        };

        vector<pair<int,int>> dirs = {{1,1},{-1,1},{1,-1},{-1,-1}};
        vector<int> cw = {2,0,3,1};

        // Прямые цепочки от 1
        for (int d=0; d<4; d++) {
            int dx = dirs[d].first, dy = dirs[d].second;
            vector<int> xs, ys;
            for (int i=0;i<n;i++) xs.push_back(i);
            for (int j=0;j<m;j++) ys.push_back(j);
            if (dx==-1) reverse(xs.begin(), xs.end());
            if (dy==-1) reverse(ys.begin(), ys.end());
            for (int i: xs) for (int j: ys) {
                int val = grid[i][j];
                int pi = i - dx, pj = j - dy;
                if (pi>=0 && pi<n && pj>=0 && pj<m && ok(grid[pi][pj], val) && end[d][pi][pj]>0)
                    end[d][i][j] = end[d][pi][pj] + 1;
                else
                    end[d][i][j] = (val==1);
            }
        }

        // Длины вперёд
        for (int d=0; d<4; d++) {
            int dx = dirs[d].first, dy = dirs[d].second;
            vector<int> xs, ys;
            for (int i=0;i<n;i++) xs.push_back(i);
            for (int j=0;j<m;j++) ys.push_back(j);
            if (dx==1) reverse(xs.begin(), xs.end());
            if (dy==1) reverse(ys.begin(), ys.end());
            for (int i: xs) for (int j: ys) {
                int ni = i+dx, nj = j+dy;
                if (ni>=0 && ni<n && nj>=0 && nj<m && ok(grid[i][j], grid[ni][nj]))
                    go[d][i][j] = 1 + go[d][ni][nj];
                else go[d][i][j] = 1;
            }
        }

        int ans=0;
        for (int d=0; d<4; d++) for (int i=0;i<n;i++) for (int j=0;j<m;j++)
            ans = max(ans, end[d][i][j]);

        for (int i=0;i<n;i++) for (int j=0;j<m;j++) for (int a=0;a<4;a++) {
            int b = cw[a];
            if (end[a][i][j]>0)
                ans = max(ans, end[a][i][j] + go[b][i][j] - 1);
        }
        return ans;
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