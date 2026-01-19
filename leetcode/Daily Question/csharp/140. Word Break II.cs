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

using System;
using System.Collections.Generic;

// Узел Trie
public class TrieNode {
    public Dictionary<char, TrieNode> Children { get; set; }
    public bool IsEnd { get; set; }
    
    public TrieNode() {
        Children = new Dictionary<char, TrieNode>();
        IsEnd = false;
    }
}

// Префиксное дерево
public class Trie {
    private TrieNode root;
    
    public Trie() {
        root = new TrieNode();
    }
    
    // Вставка слова в Trie
    public void Insert(string word) {
        TrieNode node = root;
        foreach (char c in word) {
            if (!node.Children.ContainsKey(c)) {
                node.Children[c] = new TrieNode();
            }
            node = node.Children[c];
        }
        node.IsEnd = true;
    }
    
    // Проверка существования слова
    public bool Search(string word) {
        TrieNode node = root;
        foreach (char c in word) {
            if (!node.Children.ContainsKey(c)) {
                return false;
            }
            node = node.Children[c];
        }
        return node.IsEnd;
    }
}

public class Solution {
    // Подход 1: DFS с мемоизацией и Trie (Наиболее оптимальный)
    // Время: O(n * 2^n) в худшем случае, Память: O(n * 2^n)
    public IList<string> WordBreak(string s, IList<string> wordDict) {
        /*
        Используем Trie для эффективного поиска слов и DFS с мемоизацией
        для построения всех возможных предложений.
        */
        // Строим Trie из словаря
        Trie trie = new Trie();
        foreach (string word in wordDict) {
            trie.Insert(word);
        }
        
        // Словарь для мемоизации
        Dictionary<int, List<string>> memo = new Dictionary<int, List<string>>();
        
        return DFS(s, 0, trie, memo);
    }
    
    private List<string> DFS(string s, int start, Trie trie,
                            Dictionary<int, List<string>> memo) {
        // Если достигли конца строки
        if (start == s.Length) {
            return new List<string> { "" };
        }
        
        // Если результат уже вычислен
        if (memo.ContainsKey(start)) {
            return memo[start];
        }
        
        List<string> results = new List<string>();
        
        // Пробуем все возможные слова
        for (int end = start + 1; end <= s.Length; end++) {
            string word = s.Substring(start, end - start);
            
            if (trie.Search(word)) {
                List<string> subResults = DFS(s, end, trie, memo);
                
                foreach (string sub in subResults) {
                    if (string.IsNullOrEmpty(sub)) {
                        results.Add(word);
                    } else {
                        results.Add(word + " " + sub);
                    }
                }
            }
        }
        
        memo[start] = results;
        return results;
    }
    
    // Подход 2: DFS с мемоизацией (без Trie)
    // Время: O(n * 2^n), Память: O(n * 2^n)
    public IList<string> WordBreak_Simple(string s, IList<string> wordDict) {
        /*
        Простой подход с использованием множества для словаря.
        */
        HashSet<string> wordSet = new HashSet<string>(wordDict);
        Dictionary<int, List<string>> memo = new Dictionary<int, List<string>>();
        
        return DFSSimple(s, 0, wordSet, memo);
    }
    
    private List<string> DFSSimple(string s, int start,
                                   HashSet<string> wordSet,
                                   Dictionary<int, List<string>> memo) {
        if (start == s.Length) {
            return new List<string> { "" };
        }
        
        if (memo.ContainsKey(start)) {
            return memo[start];
        }
        
        List<string> results = new List<string>();
        
        for (int end = start + 1; end <= s.Length; end++) {
            string word = s.Substring(start, end - start);
            
            if (wordSet.Contains(word)) {
                List<string> subResults = DFSSimple(s, end, wordSet, memo);
                
                foreach (string sub in subResults) {
                    if (string.IsNullOrEmpty(sub)) {
                        results.Add(word);
                    } else {
                        results.Add(word + " " + sub);
                    }
                }
            }
        }
        
        memo[start] = results;
        return results;
    }
}