/**
 * https://leetcode.com/problems/word-search-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "212. Word Search II
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

using System.Collections.Generic;

public class Solution {
    public IList<string> FindWords(char[][] board, string[] words) {
        TrieNode root = BuildTrie(words);
        List<string> result = new List<string>();
        int m = board.Length, n = board[0].Length;
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                Dfs(board, i, j, root, result);
            }
        }
        
        return result;
    }
    
    private class TrieNode {
        public Dictionary<char, TrieNode> Children = new Dictionary<char, TrieNode>();
        public string Word;
    }
    
    private TrieNode BuildTrie(string[] words) {
        TrieNode root = new TrieNode();
        
        foreach (string word in words) {
            TrieNode node = root;
            foreach (char ch in word) {
                if (!node.Children.ContainsKey(ch)) {
                    node.Children[ch] = new TrieNode();
                }
                node = node.Children[ch];
            }
            node.Word = word;
        }
        
        return root;
    }
    
    private void Dfs(char[][] board, int i, int j, TrieNode node, List<string> result) {
        char ch = board[i][j];
        
        if (!node.Children.ContainsKey(ch)) {
            return;
        }
        
        TrieNode nextNode = node.Children[ch];
        
        if (nextNode.Word != null) {
            result.Add(nextNode.Word);
            nextNode.Word = null;
        }
        
        board[i][j] = '#';
        
        if (i > 0) Dfs(board, i - 1, j, nextNode, result);
        if (j > 0) Dfs(board, i, j - 1, nextNode, result);
        if (i < board.Length - 1) Dfs(board, i + 1, j, nextNode, result);
        if (j < board[0].Length - 1) Dfs(board, i, j + 1, nextNode, result);
        
        board[i][j] = ch;
    }
}