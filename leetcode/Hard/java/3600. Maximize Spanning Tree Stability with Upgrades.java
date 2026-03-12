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
    public int maxStability(int n, int[][] edges, int k) {
        List<Edge> e = new ArrayList<>();
        for (int[] edge : edges) {
            e.add(new Edge(edge[0], edge[1], edge[2], edge[3]));
        }
        
        // Собираем все возможные значения стабильности
        Set<Integer> strengthSet = new TreeSet<>();
        for (Edge edge : e) {
            strengthSet.add(edge.s);
            if (edge.must == 0) {
                strengthSet.add(edge.s * 2);
            }
        }
        List<Integer> strengths = new ArrayList<>(strengthSet);
        
        int left = 0, right = strengths.size() - 1;
        int ans = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            int target = strengths.get(mid);
            
            if (canAchieve(n, e, k, target)) {
                ans = target;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return ans;
    }
    
    private class Edge {
        int u, v, s, must;
        Edge(int u, int v, int s, int must) {
            this.u = u;
            this.v = v;
            this.s = s;
            this.must = must;
        }
    }
    
    private class DSU {
        int[] parent;
        int[] rank;
        
        DSU(int n) {
            parent = new int[n];
            rank = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }
        
        int find(int x) {
            if (parent[x] != x) parent[x] = find(parent[x]);
            return parent[x];
        }
        
        boolean unite(int x, int y) {
            x = find(x);
            y = find(y);
            if (x == y) return false;
            if (rank[x] < rank[y]) parent[x] = y;
            else if (rank[x] > rank[y]) parent[y] = x;
            else {
                parent[y] = x;
                rank[x]++;
            }
            return true;
        }
        
        boolean isConnected() {
            int root = find(0);
            for (int i = 1; i < parent.length; i++) {
                if (find(i) != root) return false;
            }
            return true;
        }
    }
    
    private boolean canAchieve(int n, List<Edge> edges, int k, int target) {
        DSU dsu = new DSU(n);
        List<Edge> optional = new ArrayList<>();
        int mandatoryEdgesUsed = 0;
        
        // Обрабатываем обязательные рёбра
        for (Edge edge : edges) {
            if (edge.must == 1) {
                if (edge.s < target) return false;
                if (dsu.unite(edge.u, edge.v)) {
                    mandatoryEdgesUsed++;
                }
            } else {
                optional.add(edge);
            }
        }
        
        // Проверяем, не создали ли обязательные рёбра циклы
        if (mandatoryEdgesUsed < countMandatory(edges)) {
            return false;
        }
        
        // Сортируем опциональные рёбра
        optional.sort((a, b) -> {
            // Сначала те, что не требуют улучшения
            boolean aGood = a.s >= target;
            boolean bGood = b.s >= target;
            if (aGood && !bGood) return -1;
            if (!aGood && bGood) return 1;
            
            // Затем сортируем по убыванию прочности
            if (aGood) {
                return Integer.compare(b.s, a.s);
            } else {
                // Для требующих улучшения - по убыванию улучшенной прочности
                int valA = a.s * 2;
                int valB = b.s * 2;
                if (valA != valB) return Integer.compare(valB, valA);
                return Integer.compare(b.s, a.s);
            }
        });
        
        int upgradesUsed = 0;
        int totalEdgesUsed = mandatoryEdgesUsed;
        
        // Добавляем опциональные рёбра
        for (Edge edge : optional) {
            if (totalEdgesUsed == n - 1) break;
            
            boolean needUpgrade = edge.s < target;
            
            if (needUpgrade) {
                if (upgradesUsed >= k || edge.s * 2 < target) continue;
                if (dsu.unite(edge.u, edge.v)) {
                    upgradesUsed++;
                    totalEdgesUsed++;
                }
            } else {
                if (dsu.unite(edge.u, edge.v)) {
                    totalEdgesUsed++;
                }
            }
        }
        
        // Проверяем, что использовано ровно n-1 рёбер и граф связен
        return totalEdgesUsed == n - 1 && dsu.isConnected();
    }
    
    private int countMandatory(List<Edge> edges) {
        int count = 0;
        for (Edge edge : edges) {
            if (edge.must == 1) count++;
        }
        return count;
    }
}