/*
https://leetcode.com/problems/count-covered-buildings/?envType=daily-question&envId=2025-12-11

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Count Covered Buildings"

Подход:
- Для каждой строки x запоминаем min и max y
- Для каждой колонки y запоминаем min и max x
- Затем проверяем условия для каждого здания
*/

class Solution {
public:
    int countCoveredBuildings(int n, vector<vector<int>>& buildings) {
        unordered_map<int, pair<int,int>> rowBounds;
        unordered_map<int, pair<int,int>> colBounds;

        for (auto &b : buildings) {
            int x = b[0], y = b[1];
            if (!rowBounds.count(x)) rowBounds[x] = {y, y};
            else {
                rowBounds[x].first  = min(rowBounds[x].first, y);
                rowBounds[x].second = max(rowBounds[x].second, y);
            }
            if (!colBounds.count(y)) colBounds[y] = {x, x};
            else {
                colBounds[y].first  = min(colBounds[y].first, x);
                colBounds[y].second = max(colBounds[y].second, x);
            }
        }

        int ans = 0;
        for (auto &b : buildings) {
            int x = b[0], y = b[1];

            auto &rb = rowBounds[x];
            auto &cb = colBounds[y];

            if (rb.first < y && y < rb.second &&
                cb.first < x && x < cb.second) {
                ans++;
            }
        }
        return ans;
    }
};
