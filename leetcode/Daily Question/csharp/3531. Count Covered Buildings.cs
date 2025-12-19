/*
https://leetcode.com/problems/count-covered-buildings/?envType=daily-question&envId=2025-12-11

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Count Covered Buildings"

Идея:
- Для каждой строки и колонки храним минимальные и максимальные координаты.
- Здание покрыто, если его x/y строго между min и max в строке и колонке.
*/

using System;
using System.Collections.Generic;

public class Solution {
    public int CountCoveredBuildings(int n, int[][] buildings) {
        var rowMin = new Dictionary<int,int>();
        var rowMax = new Dictionary<int,int>();
        var colMin = new Dictionary<int,int>();
        var colMax = new Dictionary<int,int>();

        foreach (var b in buildings) {
            int x = b[0], y = b[1];

            if (!rowMin.ContainsKey(x)) {
                rowMin[x] = y; rowMax[x] = y;
            } else {
                rowMin[x] = Math.Min(rowMin[x], y);
                rowMax[x] = Math.Max(rowMax[x], y);
            }

            if (!colMin.ContainsKey(y)) {
                colMin[y] = x; colMax[y] = x;
            } else {
                colMin[y] = Math.Min(colMin[y], x);
                colMax[y] = Math.Max(colMax[y], x);
            }
        }

        int ans = 0;
        foreach (var b in buildings) {
            int x = b[0], y = b[1];
            if (rowMin[x] < y && y < rowMax[x] && colMin[y] < x && x < colMax[y])
                ans++;
        }

        return ans;
    }
}
