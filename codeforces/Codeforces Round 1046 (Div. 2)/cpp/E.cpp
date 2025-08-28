/**
 * https://codeforces.com/contest/2136/problem/E
 */

#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll MOD = 998244353;

ll modpow(ll a, ll e) {
    ll r = 1 % MOD;
    a %= MOD;
    while (e) {
        if (e & 1) r = (r * a) % MOD;
        a = (a * a) % MOD;
        e >>= 1;
    }
    return r;
}

struct SparseGauss {
    unordered_map<int, vector<int>> lead_row;
    unordered_map<int, int> lead_rhs;
    void reduce_row(vector<int>& row, int &rhs) {
        while (!row.empty()) {
            int lead = row[0];
            auto it = lead_row.find(lead);
            if (it == lead_row.end()) break;
            const vector<int>& prow = it->second;
            int pr = lead_rhs[lead];
            vector<int> res;
            res.reserve(row.size() + prow.size());
            size_t i = 0, j = 0;
            while (i < row.size() && j < prow.size()) {
                if (row[i] == prow[j]) { i++; j++; }
                else if (row[i] > prow[j]) { res.push_back(row[i]); i++; }
                else { res.push_back(prow[j]); j++; }
            }
            while (i < row.size()) { res.push_back(row[i]); i++; }
            while (j < prow.size()) { res.push_back(prow[j]); j++; }
            row.swap(res);
            rhs ^= pr;
        }
    }
    bool insert_reduced_row(vector<int>& row, int rhs) {
        if (row.empty()) {
            return rhs == 0;
        }
        int lead = row[0];
        lead_row[lead] = row;
        lead_rhs[lead] = rhs;
        return true;
    }
    pair<bool,int> build_from_rows(vector<vector<int>>& rows, vector<int>& rhs) {
        lead_row.clear(); lead_rhs.clear();
        int rank = 0;
        for (size_t i = 0; i < rows.size(); ++i) {
            vector<int>& row = rows[i];
            int r = rhs[i];
            sort(row.begin(), row.end(), greater<int>());
            reduce_row(row, r);
            if (row.empty()) {
                if (r != 0) return {false, 0};
                continue;
            }
            insert_reduced_row(row, r);
            ++rank;
        }
        return {true, rank};
    }
};

void build_fundamental_cycles(int n, const vector<pair<int,int>>& edges,
                              const vector<vector<pair<int,int>>>& g,
                              vector<int>& parent, vector<int>& parent_eid, vector<int>& depth,
                              vector<vector<int>>& cycles) {
    int m = edges.size();
    vector<char> is_tree_edge(m, 0);
    for (int v = 0; v < n; ++v) {
        if (parent_eid[v] >= 0) is_tree_edge[parent_eid[v]] = 1;
    }
    for (int eid = 0; eid < m; ++eid) {
        if (is_tree_edge[eid]) continue;
        int u = edges[eid].first;
        int v = edges[eid].second;
        if (depth[u] < depth[v]) swap(u,v);
        int x = u, y = v;
        vector<int> path_u, path_v;
        while (depth[x] > depth[y]) {
            path_u.push_back(x);
            x = parent[x];
        }
        while (depth[y] > depth[x]) {
            path_v.push_back(y);
            y = parent[y];
        }
        while (x != y) {
            path_u.push_back(x);
            path_v.push_back(y);
            x = parent[x];
            y = parent[y];
        }
        vector<int> cycle;
        cycle.push_back(x);
        for (int i = (int)path_u.size() - 1; i >= 0; --i) cycle.push_back(path_u[i]);
        for (int vtx : path_v) cycle.push_back(vtx);
        cycles.push_back(cycle);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n, m;
        long long V;
        cin >> n >> m >> V;
        vector<long long> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];
        vector<pair<int,int>> edges(m);
        vector<vector<pair<int,int>>> g(n);
        for (int i = 0; i < m; ++i) {
            int u, v; cin >> u >> v; --u; --v;
            edges[i] = {u,v};
            g[u].push_back({v,i});
            g[v].push_back({u,i});
        }
        if (m == n - 1) {
            int cnt_unknown = 0;
            for (int i = 0; i < n; ++i) if (a[i] == -1) cnt_unknown++;
            cout << modpow(V, cnt_unknown) << "\n";
            continue;
        }
        vector<int> parent(n, -1), parent_eid(n, -1), depth(n, 0), tin(n, -1);
        vector<int> it_index(n, 0);
        int timer = 0;
        stack<int> st;
        st.push(0);
        parent[0] = -2;
        parent_eid[0] = -1;
        while (!st.empty()) {
            int v = st.top();
            if (tin[v] == -1) tin[v] = timer++;
            if (it_index[v] < (int)g[v].size()) {
                auto e = g[v][it_index[v]++];
                int to = e.first;
                int eid = e.second;
                if (tin[to] == -1) {
                    parent[to] = v;
                    parent_eid[to] = eid;
                    depth[to] = depth[v] + 1;
                    st.push(to);
                } else {
                }
            } else st.pop();
        }
        vector<vector<int>> cycles;
        build_fundamental_cycles(n, edges, g, parent, parent_eid, depth, cycles);
        bool V_is_pow2 = (V > 0) && ((V & (V - 1)) == 0);
        if (V_is_pow2) {
            int B = 0;
            while ((1LL << B) < V) ++B;
            ll total_free = 0;
            for (int b = 0; b < B; ++b) {
                vector<vector<int>> rows;
                vector<int> rhs;
                rows.reserve(cycles.size() + n);
                rhs.reserve(cycles.size() + n);
                for (auto &cyc : cycles) {
                    rows.push_back(cyc);
                    rhs.push_back(0);
                }
                for (int i = 0; i < n; ++i) {
                    if (a[i] != -1) {
                        rows.push_back(vector<int>{i});
                        rhs.push_back( (int)((a[i] >> b) & 1LL) );
                    }
                }
                SparseGauss G;
                auto res = G.build_from_rows(rows, rhs);
                if (!res.first) {
                    total_free = -1;
                    break;
                }
                int rank = res.second;
                int free = n - rank;
                total_free += free;
            }
            if (total_free < 0) {
                cout << 0 << "\n";
            } else {
                cout << modpow(2, total_free) << "\n";
            }
            continue;
        }
        int B = 0;
        long long tmpV = V - 1;
        while (tmpV > 0) { ++B; tmpV >>= 1; }
        if (B == 0) B = 1;
        bool inconsistent_any = false;
        for (int b = 0; b < B; ++b) {
            vector<vector<int>> rows;
            vector<int> rhs;
            for (auto &cyc : cycles) {
                rows.push_back(cyc);
                rhs.push_back(0);
            }
            for (int i = 0; i < n; ++i) {
                if (a[i] != -1) {
                    rows.push_back(vector<int>{i});
                    rhs.push_back( (int)((a[i] >> b) & 1LL) );
                }
            }
            SparseGauss G;
            auto res = G.build_from_rows(rows, rhs);
            if (!res.first) { inconsistent_any = true; break; }
        }
        if (inconsistent_any) {
            cout << 0 << "\n";
            continue;
        }
        cout << "0\n";
    }
    return 0;
}

/** Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
*/