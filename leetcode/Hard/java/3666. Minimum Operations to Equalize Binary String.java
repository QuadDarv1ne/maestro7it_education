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
    public int minOperations(String s, int k) {
        int n = s.length();
        int z0 = 0;
        for (char c : s.toCharArray()) if (c == '0') z0++;
        if (z0 == 0) return 0;

        int[] parentEven = new int[n + 3];
        int[] parentOdd = new int[n + 3];
        for (int i = 0; i < n + 3; i++) {
            parentEven[i] = i;
            parentOdd[i] = i;
        }

        Queue<int[]> q = new LinkedList<>();
        q.add(new int[]{z0, 0});
        markVisited(parentEven, parentOdd, z0);

        while (!q.isEmpty()) {
            int[] cur = q.poll();
            int z = cur[0];
            int dist = cur[1];

            int max_i = Math.min(k, z);
            int min_i = Math.max(0, k - (n - z));
            int low = z + k - 2 * max_i;
            int high = z + k - 2 * min_i;
            if (low > high) continue;

            int targetParity = (z + k) % 2;
            int[] parent = targetParity == 0 ? parentEven : parentOdd;

            if (low % 2 != targetParity) low++;
            if (low > high) continue;

            int x = find(parent, low);
            while (x <= high && x <= n) {
                if (x == 0) return dist + 1;
                q.add(new int[]{x, dist + 1});
                parent[x] = find(parent, x + 2);
                x = find(parent, x);
            }
        }
        return -1;
    }

    private int find(int[] parent, int x) {
        if (parent[x] != x) parent[x] = find(parent, parent[x]);
        return parent[x];
    }

    private void markVisited(int[] parentEven, int[] parentOdd, int z) {
        if (z % 2 == 0) {
            parentEven[z] = find(parentEven, z + 2);
        } else {
            parentOdd[z] = find(parentOdd, z + 2);
        }
    }
}