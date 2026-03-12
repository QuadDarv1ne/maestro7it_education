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
    public int MaxStability(int n, int[][] edges, int k) {
        var e = new List<(int u, int v, int s, int must)>();
        foreach (var edge in edges) {
            e.Add((edge[0], edge[1], edge[2], edge[3]));
        }
        
        // Собираем все возможные значения стабильности
        var strengths = new List<int>();
        foreach (var edge in e) {
            strengths.Add(edge.s);
            if (edge.must == 0) {
                strengths.Add(edge.s * 2);
            }
        }
        strengths = strengths.Distinct().OrderBy(x => x).ToList();
        
        int left = 0, right = strengths.Count - 1;
        int ans = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            int target = strengths[mid];
            
            if (CanAchieve(n, e, k, target)) {
                ans = target;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return ans;
    }
    
    private class DSU {
        private int[] parent;
        private int[] rank;
        
        public DSU(int n) {
            parent = new int[n];
            rank = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }
        
        public int Find(int x) {
            if (parent[x] != x) parent[x] = Find(parent[x]);
            return parent[x];
        }
        
        public bool Unite(int x, int y) {
            x = Find(x);
            y = Find(y);
            if (x == y) return false;
            if (rank[x] < rank[y]) parent[x] = y;
            else if (rank[x] > rank[y]) parent[y] = x;
            else {
                parent[y] = x;
                rank[x]++;
            }
            return true;
        }
        
        public bool IsConnected() {
            int root = Find(0);
            for (int i = 1; i < parent.Length; i++) {
                if (Find(i) != root) return false;
            }
            return true;
        }
    }
    
    private bool CanAchieve(int n, List<(int u, int v, int s, int must)> edges, int k, int target) {
        var dsu = new DSU(n);
        var optional = new List<(int u, int v, int s)>();
        int mandatoryUsed = 0;
        int mandatoryCount = 0;
        
        foreach (var edge in edges) {
            if (edge.must == 1) {
                mandatoryCount++;
                if (edge.s < target) return false;
                if (dsu.Unite(edge.u, edge.v)) {
                    mandatoryUsed++;
                }
            } else {
                optional.Add((edge.u, edge.v, edge.s));
            }
        }
        
        // Проверяем, не создали ли обязательные рёбра циклы
        if (mandatoryUsed < mandatoryCount) return false;
        
        // Сортируем опциональные рёбра: сначала те, что не требуют улучшения
        optional = optional
            .OrderByDescending(e => e.s >= target) // Сначала те, что >= target
            .ThenByDescending(e => e.s) // Затем по убыванию прочности
            .ToList();
        
        int upgradesUsed = 0;
        int totalUsed = mandatoryUsed;
        
        foreach (var edge in optional) {
            if (totalUsed == n - 1) break;
            
            if (edge.s >= target) {
                if (dsu.Unite(edge.u, edge.v)) {
                    totalUsed++;
                }
            } else if (upgradesUsed < k && edge.s * 2 >= target) {
                if (dsu.Unite(edge.u, edge.v)) {
                    upgradesUsed++;
                    totalUsed++;
                }
            }
        }
        
        return totalUsed == n - 1 && dsu.IsConnected();
    }
}