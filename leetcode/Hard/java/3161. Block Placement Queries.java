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
    /*
     * Обрабатывает запросы двух типов в обратном порядке:
     * 1: [1, x] — установить препятствие в точке x.
     * 2: [2, x, sz] — проверить, можно ли разместить блок размера sz на отрезке [0, x].
     */
    public List<Boolean> getResults(int[][] queries) {
        int n = Math.min(50000, queries.length * 3);
        int[] tree = new int[n + 1]; // Дерево Фенвика
        
        // Собираем все препятствия
        TreeSet<Integer> obstacleSet = new TreeSet<>();
        obstacleSet.add(0);
        obstacleSet.add(n);
        
        for (int[] q : queries) {
            if (q[0] == 1) {
                int x = q[1];
                if (x > 0 && x < n) {
                    obstacleSet.add(x);
                }
            }
        }
        
        List<Integer> obstacles = new ArrayList<>(obstacleSet);
        
        // Начальное заполнение дерева Фенвика
        for (int i = 1; i < obstacles.size(); i++) {
            int x1 = obstacles.get(i - 1);
            int x2 = obstacles.get(i);
            fenwickMaximize(tree, x2, x2 - x1);
        }
        
        List<Boolean> ans = new ArrayList<>();
        
        // Обрабатываем запросы с конца
        for (int i = queries.length - 1; i >= 0; i--) {
            if (queries[i][0] == 1) {
                int x = queries[i][1];
                if (x == 0 || x >= n) continue;
                
                int idx = Collections.binarySearch(obstacles, x);
                if (idx > 0 && idx < obstacles.size() - 1) {
                    int leftObstacle = obstacles.get(idx - 1);
                    int rightObstacle = obstacles.get(idx + 1);
                    
                    obstacles.remove(idx);
                    fenwickMaximize(tree, rightObstacle, rightObstacle - leftObstacle);
                }
            } else {
                int x = queries[i][1];
                int sz = queries[i][2];
                
                int idx = Collections.binarySearch(obstacles, x);
                if (idx < 0) idx = -idx - 1;
                int leftObstacle = obstacles.get(idx - 1);
                
                ans.add(fenwickGet(tree, leftObstacle) >= sz || x - leftObstacle >= sz);
            }
        }
        
        Collections.reverse(ans);
        return ans;
    }
    
    private void fenwickMaximize(int[] tree, int i, int val) {
        while (i < tree.length) {
            tree[i] = Math.max(tree[i], val);
            i += i & -i;
        }
    }
    
    private int fenwickGet(int[] tree, int i) {
        int res = 0;
        while (i > 0) {
            res = Math.max(res, tree[i]);
            i -= i & -i;
        }
        return res;
    }
}