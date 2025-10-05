/*
https://leetcode.com/problems/pacific-atlantic-water-flow/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

using System;
using System.Collections.Generic;

public class Solution {
    private int m, n;
    private int[][] heights;
    private readonly int[][] dirs = new int[][] {
        new int[]{1,0}, new int[]{-1,0}, new int[]{0,1}, new int[]{0,-1}
    };

    public IList<IList<int>> PacificAtlantic(int[][] heights) {
        this.heights = heights;
        m = heights.Length;
        n = heights[0].Length;

        bool[][] pac = CreateBoolMatrix(m, n);
        bool[][] atl = CreateBoolMatrix(m, n);

        for (int i = 0; i < m; i++) {
            Dfs(i, 0, pac);
            Dfs(i, n - 1, atl);
        }
        for (int j = 0; j < n; j++) {
            Dfs(0, j, pac);
            Dfs(m - 1, j, atl);
        }

        var res = new List<IList<int>>();
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (pac[i][j] && atl[i][j])
                    res.Add(new List<int>{ i, j });
        return res;
    }

    private void Dfs(int x, int y, bool[][] visited) {
        visited[x][y] = true;
        foreach (var d in dirs) {
            int nx = x + d[0], ny = y + d[1];
            if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
            if (visited[nx][ny]) continue;
            if (heights[nx][ny] < heights[x][y]) continue;
            Dfs(nx, ny, visited);
        }
    }

    private bool[][] CreateBoolMatrix(int m, int n) {
        var mat = new bool[m][];
        for (int i = 0; i < m; i++) mat[i] = new bool[n];
        return mat;
    }
}

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