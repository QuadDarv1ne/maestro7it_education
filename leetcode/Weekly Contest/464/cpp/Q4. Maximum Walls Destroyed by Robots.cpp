/**
 * https://leetcode.com/contest/weekly-contest-464/problems/maximum-walls-destroyed-by-robots/description/
 */

class Solution {
public:
    int maxWalls(vector<int>& robots, vector<int>& distance, vector<int>& walls) {
        
        int m = robots.size();
        vector<pair<int,int>> a;
        a.reserve(m);
        for (int i = 0; i < m; ++i) a.emplace_back(robots[i], distance[i]);
        sort(a.begin(), a.end());
        vector<int> r(m), d(m);
        for (int i = 0; i < m; ++i) { r[i] = a[i].first; d[i] = a[i].second; }
        sort(walls.begin(), walls.end());
        unordered_set<int> S;
        S.reserve(m * 2);
        for (int x : r) S.insert(x);
        vector<int> v;
        v.reserve(walls.size());
        int base = 0;
        for (int x : walls) if (S.count(x)) ++base; else v.push_back(x);
        int n = v.size();
        auto lb = [&](int x) { return int(lower_bound(v.begin(), v.end(), x) - v.begin()); };
        auto ub = [&](int x) { return int(upper_bound(v.begin(), v.end(), x) - v.begin()); };
        int L0 = 0;
        if (m > 0) {
            int lo = r[0] - d[0];
            int a0 = lb(r[0]);
            int b0 = lb(lo);
            L0 = max(0, a0 - b0);
        }
        int Rlast = 0;
        if (m > 0) {
            int rn = r[m - 1];
            int lo = ub(rn);
            int hi = ub(rn + d[m - 1]);
            Rlast = max(0, hi - lo);
        }
        vector<int> A(max(0, m - 1)), B(max(0, m - 1)), AB(max(0, m - 1));
        for (int j = 0; j + 1 < m; ++j) {
            int p = r[j], q = r[j + 1];
            int s = lb(p + 1), e = lb(q);
            if (s >= e) { A[j] = B[j] = AB[j] = 0; continue; }
            int up = min(q - 1, p + d[j]);
            if (up < p + 1) A[j] = 0; else A[j] = max(0, lb(up + 1) - s);
            int low = max(p + 1, q - d[j + 1]);
            if (low > q - 1) B[j] = 0; else B[j] = max(0, e - lb(low));
            int lo2 = max(p + 1, q - d[j + 1]);
            int hi2 = min(q - 1, p + d[j]);
            if (lo2 > hi2) AB[j] = 0; else AB[j] = max(0, lb(hi2 + 1) - lb(lo2));
        }
        int p0 = L0, p1 = 0;
        for (int i = 1; i < m; ++i) {
            int j = i - 1;
            int c0 = max(p0 + B[j], p1 + (A[j] + B[j] - AB[j]));
            int c1 = max(p0 + 0, p1 + A[j]);
            p0 = c0; p1 = c1;
        }
        int ans = max(p0, p1 + Rlast);
        return ans + base;
    }
};

/* Полезные ссылки: */
// 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
// 2. 💠Telegram №1💠 @quadd4rv1n7
// 3. 💠Telegram №2💠 @dupley_maxim_1999
// 4. Rutube канал: https://rutube.ru/channel/4218729/
// 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
// 6. YouTube канал: https://www.youtube.com/@it-coders
// 7. ВК группа: https://vk.com/science_geeks