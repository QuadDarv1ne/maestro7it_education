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

import java.util.*;

class Solution {
    private static class TrieNode {
        Map<Character, TrieNode> children = new HashMap<>();
        List<Integer> ids = new ArrayList<>();
    }
    
    private static class Pair {
        int length;
        int id;
        
        Pair(int length, int id) {
            this.length = length;
            this.id = id;
        }
    }
    
    private TrieNode buildTrie(Set<String> strings, Map<String, Integer> strToId) {
        TrieNode root = new TrieNode();
        for (String s : strings) {
            TrieNode node = root;
            for (char ch : s.toCharArray()) {
                node.children.putIfAbsent(ch, new TrieNode());
                node = node.children.get(ch);
            }
            node.ids.add(strToId.get(s));
        }
        return root;
    }
    
    private List<Pair> findMatches(TrieNode trie, String s, int start) {
        List<Pair> matches = new ArrayList<>();
        TrieNode node = trie;
        int pos = start;
        
        while (pos < s.length() && node.children.containsKey(s.charAt(pos))) {
            node = node.children.get(s.charAt(pos));
            pos++;
            if (!node.ids.isEmpty()) {
                for (int id : node.ids) {
                    matches.add(new Pair(pos - start, id));
                }
            }
        }
        return matches;
    }
    
    public long minimumCost(String source, String target, String[] original, 
                            String[] changed, int[] cost) {
        // Создание уникальных ID для строк
        Set<String> unique = new HashSet<>();
        for (String s : original) unique.add(s);
        for (String s : changed) unique.add(s);
        
        Map<String, Integer> strToId = new HashMap<>();
        int idx = 0;
        for (String s : unique) {
            strToId.put(s, idx++);
        }
        
        int n = unique.size();
        final long INF = Long.MAX_VALUE / 2;
        
        // Матрица расстояний
        long[][] dist = new long[n][n];
        for (int i = 0; i < n; i++) {
            Arrays.fill(dist[i], INF);
            dist[i][i] = 0;
        }
        
        for (int i = 0; i < original.length; i++) {
            int sid = strToId.get(original[i]);
            int tid = strToId.get(changed[i]);
            dist[sid][tid] = Math.min(dist[sid][tid], cost[i]);
        }
        
        // Floyd-Warshall
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                if (dist[i][k] < INF) {
                    for (int j = 0; j < n; j++) {
                        if (dist[k][j] < INF) {
                            dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
                        }
                    }
                }
            }
        }
        
        // Построение Trie
        TrieNode srcTrie = buildTrie(unique, strToId);
        TrieNode tgtTrie = buildTrie(unique, strToId);
        
        // DP
        int m = source.length();
        long[] dp = new long[m + 1];
        Arrays.fill(dp, INF);
        dp[m] = 0;
        
        for (int i = m - 1; i >= 0; i--) {
            if (source.charAt(i) == target.charAt(i) && dp[i + 1] < INF) {
                dp[i] = dp[i + 1];
            }
            
            List<Pair> srcMatches = findMatches(srcTrie, source, i);
            List<Pair> tgtMatches = findMatches(tgtTrie, target, i);
            
            Map<Integer, List<Integer>> tgtByLen = new HashMap<>();
            for (Pair p : tgtMatches) {
                tgtByLen.computeIfAbsent(p.length, k -> new ArrayList<>()).add(p.id);
            }
            
            for (Pair srcPair : srcMatches) {
                int srcLen = srcPair.length;
                int sid = srcPair.id;
                
                if (tgtByLen.containsKey(srcLen) && dp[i + srcLen] < INF) {
                    for (int tid : tgtByLen.get(srcLen)) {
                        if (dist[sid][tid] < INF) {
                            dp[i] = Math.min(dp[i], dist[sid][tid] + dp[i + srcLen]);
                        }
                    }
                }
            }
        }
        
        return dp[0] < INF ? dp[0] : -1;
    }
}