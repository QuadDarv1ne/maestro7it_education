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

class Solution {
public:
    int minOperations(string s, int k) {
        int n = s.size();
        int z0 = count(s.begin(), s.end(), '0');
        if (z0 == 0) return 0;

        vector<int> parent_even(n + 3), parent_odd(n + 3);
        for (int i = 0; i < n + 3; ++i) {
            parent_even[i] = i;
            parent_odd[i] = i;
        }

        function<int(vector<int>&, int)> find = [&](vector<int>& parent, int x) -> int {
            if (parent[x] != x) parent[x] = find(parent, parent[x]);
            return parent[x];
        };

        auto mark_visited = [&](int z) {
            if (z % 2 == 0) parent_even[z] = find(parent_even, z + 2);
            else parent_odd[z] = find(parent_odd, z + 2);
        };

        queue<pair<int, int>> q;
        q.push({z0, 0});
        mark_visited(z0);

        while (!q.empty()) {
            auto [z, dist] = q.front(); q.pop();

            int max_i = min(k, z);
            int min_i = max(0, k - (n - z));
            int low = z + k - 2 * max_i;
            int high = z + k - 2 * min_i;
            if (low > high) continue;

            int target_parity = (z + k) % 2;
            vector<int>& parent = (target_parity == 0) ? parent_even : parent_odd;

            if (low % 2 != target_parity) low++;
            if (low > high) continue;

            int x = find(parent, low);
            while (x <= high && x <= n) {
                if (x == 0) return dist + 1;
                q.push({x, dist + 1});
                parent[x] = find(parent, x + 2);
                x = find(parent, x);
            }
        }
        return -1;
    }
};