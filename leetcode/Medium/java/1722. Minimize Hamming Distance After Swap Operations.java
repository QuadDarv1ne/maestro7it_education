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

import java.util.*;

class Solution {
    private int[] parent, rank;

    private int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    private void union(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return;
        if (rank[rx] < rank[ry]) parent[rx] = ry;
        else if (rank[rx] > rank[ry]) parent[ry] = rx;
        else { parent[ry] = rx; rank[rx]++; }
    }

    public int minimumHammingDistance(int[] source, int[] target, int[][] allowedSwaps) {
        int n = source.length;
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;

        for (int[] sw : allowedSwaps) union(sw[0], sw[1]);

        Map<Integer, Map<Integer, Integer>> compCount = new HashMap<>();
        for (int i = 0; i < n; i++) {
            int root = find(i);
            compCount.putIfAbsent(root, new HashMap<>());
            Map<Integer, Integer> cnt = compCount.get(root);
            cnt.put(source[i], cnt.getOrDefault(source[i], 0) + 1);
        }

        int ans = 0;
        for (int i = 0; i < n; i++) {
            int root = find(i);
            Map<Integer, Integer> cnt = compCount.get(root);
            if (cnt.containsKey(target[i]) && cnt.get(target[i]) > 0) {
                cnt.put(target[i], cnt.get(target[i]) - 1);
            } else ans++;
        }
        return ans;
    }
}