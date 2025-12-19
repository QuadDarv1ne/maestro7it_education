/*
https://leetcode.com/problems/count-covered-buildings/?envType=daily-question&envId=2025-12-11

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Count Covered Buildings"
*/

import java.util.*;

class Solution {
    public int countCoveredBuildings(int n, int[][] buildings) {
        Map<Integer,Integer> rowMin = new HashMap<>();
        Map<Integer,Integer> rowMax = new HashMap<>();
        Map<Integer,Integer> colMin = new HashMap<>();
        Map<Integer,Integer> colMax = new HashMap<>();

        for (int[] b : buildings) {
            int x = b[0], y = b[1];

            rowMin.put(x, rowMin.containsKey(x) ? Math.min(rowMin.get(x), y) : y);
            rowMax.put(x, rowMax.containsKey(x) ? Math.max(rowMax.get(x), y) : y);

            colMin.put(y, colMin.containsKey(y) ? Math.min(colMin.get(y), x) : x);
            colMax.put(y, colMax.containsKey(y) ? Math.max(colMax.get(y), x) : x);
        }

        int ans = 0;
        for (int[] b : buildings) {
            int x = b[0], y = b[1];
            if (rowMin.get(x) < y && y < rowMax.get(x) &&
                colMin.get(y) < x && x < colMax.get(y))
                ans++;
        }

        return ans;
    }
}
