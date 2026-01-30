/*
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
 
Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
*/

using System;
using System.Collections.Generic;
using System.Linq;

public class Solution {
    private class TrieNode {
        public Dictionary<char, TrieNode> Children = new Dictionary<char, TrieNode>();
        public List<int> Ids = new List<int>();
    }
    
    private TrieNode BuildTrie(HashSet<string> strings, Dictionary<string, int> strToId) {
        TrieNode root = new TrieNode();
        foreach (string s in strings) {
            TrieNode node = root;
            foreach (char ch in s) {
                if (!node.Children.ContainsKey(ch)) {
                    node.Children[ch] = new TrieNode();
                }
                node = node.Children[ch];
            }
            node.Ids.Add(strToId[s]);
        }
        return root;
    }
    
    private List<(int, int)> FindMatches(TrieNode trie, string s, int start) {
        List<(int, int)> matches = new List<(int, int)>();
        TrieNode node = trie;
        int pos = start;
        
        while (pos < s.Length && node.Children.ContainsKey(s[pos])) {
            node = node.Children[s[pos]];
            pos++;
            if (node.Ids.Count > 0) {
                foreach (int id in node.Ids) {
                    matches.Add((pos - start, id));
                }
            }
        }
        return matches;
    }
    
    public long MinimumCost(string source, string target, string[] original, 
                            string[] changed, int[] cost) {
        // Создание уникальных ID для строк
        HashSet<string> unique = new HashSet<string>(original.Concat(changed));
        Dictionary<string, int> strToId = new Dictionary<string, int>();
        int idx = 0;
        foreach (string s in unique) {
            strToId[s] = idx++;
        }
        
        int n = unique.Count;
        const long INF = long.MaxValue / 2;
        
        // Матрица расстояний
        long[,] dist = new long[n, n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                dist[i, j] = INF;
            }
            dist[i, i] = 0;
        }
        
        for (int i = 0; i < original.Length; i++) {
            int sid = strToId[original[i]];
            int tid = strToId[changed[i]];
            dist[sid, tid] = Math.Min(dist[sid, tid], cost[i]);
        }
        
        // Floyd-Warshall
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                if (dist[i, k] < INF) {
                    for (int j = 0; j < n; j++) {
                        if (dist[k, j] < INF) {
                            dist[i, j] = Math.Min(dist[i, j], dist[i, k] + dist[k, j]);
                        }
                    }
                }
            }
        }
        
        // Построение Trie
        TrieNode srcTrie = BuildTrie(unique, strToId);
        TrieNode tgtTrie = BuildTrie(unique, strToId);
        
        // DP
        int m = source.Length;
        long[] dp = new long[m + 1];
        Array.Fill(dp, INF);
        dp[m] = 0;
        
        for (int i = m - 1; i >= 0; i--) {
            if (source[i] == target[i] && dp[i + 1] < INF) {
                dp[i] = dp[i + 1];
            }
            
            var srcMatches = FindMatches(srcTrie, source, i);
            var tgtMatches = FindMatches(tgtTrie, target, i);
            
            Dictionary<int, List<int>> tgtByLen = new Dictionary<int, List<int>>();
            foreach (var (len, tid) in tgtMatches) {
                if (!tgtByLen.ContainsKey(len)) {
                    tgtByLen[len] = new List<int>();
                }
                tgtByLen[len].Add(tid);
            }
            
            foreach (var (srcLen, sid) in srcMatches) {
                if (tgtByLen.ContainsKey(srcLen) && dp[i + srcLen] < INF) {
                    foreach (int tid in tgtByLen[srcLen]) {
                        if (dist[sid, tid] < INF) {
                            dp[i] = Math.Min(dp[i], dist[sid, tid] + dp[i + srcLen]);
                        }
                    }
                }
            }
        }
        
        return dp[0] < INF ? dp[0] : -1;
    }
}