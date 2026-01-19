/*
LeetCode 140: Word Break II

Задача: Дана строка s и словарь строк wordDict. Добавьте пробелы в s, чтобы
построить предложение, где каждое слово является допустимым словом из словаря.
Верните все такие возможные предложения в любом порядке.

Примечание: Одно и то же слово из словаря может быть использовано несколько раз.

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1: @quadd4rv1n7
3. Telegram №2: @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
*/

import java.util.*;

// Узел Trie
class TrieNode {
    Map<Character, TrieNode> children;
    boolean isEnd;
    
    public TrieNode() {
        children = new HashMap<>();
        isEnd = false;
    }
}

// Префиксное дерево
class Trie {
    private TrieNode root;
    
    public Trie() {
        root = new TrieNode();
    }
    
    // Вставка слова в Trie
    public void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            node.children.putIfAbsent(c, new TrieNode());
            node = node.children.get(c);
        }
        node.isEnd = true;
    }
    
    // Проверка существования слова
    public boolean search(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            if (!node.children.containsKey(c)) {
                return false;
            }
            node = node.children.get(c);
        }
        return node.isEnd;
    }
}

class Solution {
    // Подход 1: DFS с мемоизацией и Trie (Наиболее оптимальный)
    // Время: O(n * 2^n) в худшем случае, Память: O(n * 2^n)
    public List<String> wordBreak(String s, List<String> wordDict) {
        /*
        Используем Trie для эффективного поиска слов и DFS с мемоизацией
        для построения всех возможных предложений.
        */
        // Строим Trie из словаря
        Trie trie = new Trie();
        for (String word : wordDict) {
            trie.insert(word);
        }
        
        // Словарь для мемоизации
        Map<Integer, List<String>> memo = new HashMap<>();
        
        return dfs(s, 0, trie, memo);
    }
    
    private List<String> dfs(String s, int start, Trie trie,
                            Map<Integer, List<String>> memo) {
        // Если достигли конца строки
        if (start == s.length()) {
            List<String> result = new ArrayList<>();
            result.add("");
            return result;
        }
        
        // Если результат уже вычислен
        if (memo.containsKey(start)) {
            return memo.get(start);
        }
        
        List<String> results = new ArrayList<>();
        
        // Пробуем все возможные слова
        for (int end = start + 1; end <= s.length(); end++) {
            String word = s.substring(start, end);
            
            if (trie.search(word)) {
                List<String> subResults = dfs(s, end, trie, memo);
                
                for (String sub : subResults) {
                    if (sub.isEmpty()) {
                        results.add(word);
                    } else {
                        results.add(word + " " + sub);
                    }
                }
            }
        }
        
        memo.put(start, results);
        return results;
    }
    
    // Подход 2: DFS с мемоизацией (без Trie)
    // Время: O(n * 2^n), Память: O(n * 2^n)
    public List<String> wordBreakSimple(String s, List<String> wordDict) {
        /*
        Простой подход с использованием множества для словаря.
        */
        Set<String> wordSet = new HashSet<>(wordDict);
        Map<Integer, List<String>> memo = new HashMap<>();
        
        return dfsSimple(s, 0, wordSet, memo);
    }
    
    private List<String> dfsSimple(String s, int start,
                                   Set<String> wordSet,
                                   Map<Integer, List<String>> memo) {
        if (start == s.length()) {
            List<String> result = new ArrayList<>();
            result.add("");
            return result;
        }
        
        if (memo.containsKey(start)) {
            return memo.get(start);
        }
        
        List<String> results = new ArrayList<>();
        
        for (int end = start + 1; end <= s.length(); end++) {
            String word = s.substring(start, end);
            
            if (wordSet.contains(word)) {
                List<String> subResults = dfsSimple(s, end, wordSet, memo);
                
                for (String sub : subResults) {
                    if (sub.isEmpty()) {
                        results.add(word);
                    } else {
                        results.add(word + " " + sub);
                    }
                }
            }
        }
        
        memo.put(start, results);
        return results;
    }
}