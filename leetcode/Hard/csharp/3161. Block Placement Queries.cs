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
    /*
     * Обрабатывает запросы двух типов в обратном порядке:
     * 1: [1, x] — установить препятствие в точке x.
     * 2: [2, x, sz] — проверить, можно ли разместить блок размера sz на отрезке [0, x].
     */
    public bool[] GetResults(int[][] queries) {
        int n = Math.Min(50000, queries.Length * 3);
        int[] tree = new int[n + 1]; // Дерево Фенвика
        
        void FenwickMaximize(int i, int val) {
            while (i <= n) {
                tree[i] = Math.Max(tree[i], val);
                i += i & -i;
            }
        }
        
        int FenwickGet(int i) {
            int res = 0;
            while (i > 0) {
                res = Math.Max(res, tree[i]);
                i -= i & -i;
            }
            return res;
        }
        
        // Собираем все препятствия
        SortedSet<int> obstacleSet = new SortedSet<int> { 0, n };
        foreach (var q in queries) {
            if (q[0] == 1) {
                int x = q[1];
                if (x > 0 && x < n) {
                    obstacleSet.Add(x);
                }
            }
        }
        
        List<int> obstacles = new List<int>(obstacleSet);
        
        // Начальное заполнение дерева
        for (int i = 1; i < obstacles.Count; i++) {
            int x1 = obstacles[i - 1];
            int x2 = obstacles[i];
            FenwickMaximize(x2, x2 - x1);
        }
        
        List<bool> ans = new List<bool>();
        
        // Обрабатываем запросы с конца
        for (int i = queries.Length - 1; i >= 0; i--) {
            if (queries[i][0] == 1) {
                int x = queries[i][1];
                if (x == 0 || x >= n) continue;
                
                int idx = obstacles.BinarySearch(x);
                if (idx > 0 && idx < obstacles.Count - 1) {
                    int leftObstacle = obstacles[idx - 1];
                    int rightObstacle = obstacles[idx + 1];
                    
                    obstacles.RemoveAt(idx);
                    FenwickMaximize(rightObstacle, rightObstacle - leftObstacle);
                }
            } else {
                int x = queries[i][1];
                int sz = queries[i][2];
                
                int idx = obstacles.BinarySearch(x);
                if (idx < 0) idx = ~idx;
                int leftObstacle = obstacles[idx - 1];
                
                ans.Add(FenwickGet(leftObstacle) >= sz || x - leftObstacle >= sz);
            }
        }
        
        ans.Reverse();
        return ans.ToArray();
    }
}