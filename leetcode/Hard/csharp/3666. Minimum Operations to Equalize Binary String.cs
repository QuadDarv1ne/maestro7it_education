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

public class Solution {
    public int MinOperations(string s, int k) {
        int n = s.Length;
        int z0 = s.Count(c => c == '0');
        if (z0 == 0) return 0;

        int[] parentEven = new int[n + 3];
        int[] parentOdd = new int[n + 3];
        for (int i = 0; i < n + 3; i++) {
            parentEven[i] = i;
            parentOdd[i] = i;
        }

        Func<int[], int, int> find = null;
        find = (parent, x) => {
            if (parent[x] != x) parent[x] = find(parent, parent[x]);
            return parent[x];
        };

        Action<int> markVisited = (z) => {
            if (z % 2 == 0) parentEven[z] = find(parentEven, z + 2);
            else parentOdd[z] = find(parentOdd, z + 2);
        };

        Queue<(int, int)> q = new Queue<(int, int)>();
        q.Enqueue((z0, 0));
        markVisited(z0);

        while (q.Count > 0) {
            var (z, dist) = q.Dequeue();

            int max_i = Math.Min(k, z);
            int min_i = Math.Max(0, k - (n - z));
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
                q.Enqueue((x, dist + 1));
                parent[x] = find(parent, x + 2);
                x = find(parent, x);
            }
        }
        return -1;
    }
}