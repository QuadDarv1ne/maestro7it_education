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

using System;
using System.Collections.Generic;
using System.Linq;

public class Solution {
    public int MinimumHammingDistance(int[] source, int[] target, int[][] allowedSwaps) {
        int n = source.Length;
        int[] parent = Enumerable.Range(0, n).ToArray();
        int[] rank = new int[n];

        int Find(int x) {
            if (parent[x] != x) parent[x] = Find(parent[x]);
            return parent[x];
        }

        void Union(int x, int y) {
            int rx = Find(x), ry = Find(y);
            if (rx == ry) return;
            if (rank[rx] < rank[ry]) parent[rx] = ry;
            else if (rank[rx] > rank[ry]) parent[ry] = rx;
            else { parent[ry] = rx; rank[rx]++; }
        }

        foreach (var sw in allowedSwaps) Union(sw[0], sw[1]);

        var compCount = new Dictionary<int, Dictionary<int, int>>();
        for (int i = 0; i < n; i++) {
            int root = Find(i);
            if (!compCount.ContainsKey(root)) compCount[root] = new Dictionary<int, int>();
            if (!compCount[root].ContainsKey(source[i])) compCount[root][source[i]] = 0;
            compCount[root][source[i]]++;
        }

        int ans = 0;
        for (int i = 0; i < n; i++) {
            int root = Find(i);
            var cnt = compCount[root];
            if (cnt.ContainsKey(target[i]) && cnt[target[i]] > 0) cnt[target[i]]--;
            else ans++;
        }
        return ans;
    }
}