/**
 * https://leetcode.com/problems/maximum-number-of-k-divisible-components/description/?envType=daily-question&envId=2025-11-28
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Maximum Number of K-Divisible Components" на C#
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

public class Solution {
    private List<int>[] graph;
    private int[] values;
    private int k;
    private int components;
    
    public int MaxKDivisibleComponents(int n, int[][] edges, int[] values, int k) {
        // Инициализация графа
        this.graph = new List<int>[n];
        for (int i = 0; i < n; i++) {
            graph[i] = new List<int>();
        }
        foreach (var edge in edges) {
            int u = edge[0], v = edge[1];
            graph[u].Add(v);
            graph[v].Add(u);
        }
        
        this.values = values;
        this.k = k;
        this.components = 0;
        
        DFS(0, -1);
        return components;
    }
    
    private long DFS(int node, int parent) {
        long total = values[node];
        
        foreach (int neighbor in graph[node]) {
            if (neighbor != parent) {
                total += DFS(neighbor, node);
            }
        }
        
        if (total % k == 0) {
            components++;
        }
        
        return total;
    }
}