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

import java.util.*;

class Solution {
    public List<String> findWords(char[][] board, String[] words) {
        TrieNode root = buildTrie(words);
        List<String> result = new ArrayList<>();
        int m = board.length, n = board[0].length;
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                dfs(board, i, j, root, result);
            }
        }
        
        return result;
    }
    
    class TrieNode {
        Map<Character, TrieNode> children = new HashMap<>();
        String word = null;
    }
    
    private TrieNode buildTrie(String[] words) {
        TrieNode root = new TrieNode();
        
        for (String word : words) {
            TrieNode node = root;
            for (char ch : word.toCharArray()) {
                if (!node.children.containsKey(ch)) {
                    node.children.put(ch, new TrieNode());
                }
                node = node.children.get(ch);
            }
            node.word = word;
        }
        
        return root;
    }
    
    private void dfs(char[][] board, int i, int j, TrieNode node, List<String> result) {
        char ch = board[i][j];
        
        if (!node.children.containsKey(ch)) {
            return;
        }
        
        TrieNode nextNode = node.children.get(ch);
        
        if (nextNode.word != null) {
            result.add(nextNode.word);
            nextNode.word = null;
        }
        
        board[i][j] = '#';
        
        if (i > 0) dfs(board, i - 1, j, nextNode, result);
        if (j > 0) dfs(board, i, j - 1, nextNode, result);
        if (i < board.length - 1) dfs(board, i + 1, j, nextNode, result);
        if (j < board[0].length - 1) dfs(board, i, j + 1, nextNode, result);
        
        board[i][j] = ch;
    }
}