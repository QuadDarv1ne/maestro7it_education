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

#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <iostream>

using namespace std;

// Узел Trie
struct TrieNode {
    unordered_map<char, TrieNode*> children;
    bool isEnd;
    
    TrieNode() : isEnd(false) {}
};

// Префиксное дерево
class Trie {
private:
    TrieNode* root;
    
public:
    Trie() {
        root = new TrieNode();
    }
    
    // Вставка слова в Trie
    void insert(const string& word) {
        TrieNode* node = root;
        for (char c : word) {
            if (node->children.find(c) == node->children.end()) {
                node->children[c] = new TrieNode();
            }
            node = node->children[c];
        }
        node->isEnd = true;
    }
    
    // Проверка существования слова
    bool search(const string& word) {
        TrieNode* node = root;
        for (char c : word) {
            if (node->children.find(c) == node->children.end()) {
                return false;
            }
            node = node->children[c];
        }
        return node->isEnd;
    }
    
    ~Trie() {
        deleteTrie(root);
    }
    
private:
    void deleteTrie(TrieNode* node) {
        if (!node) return;
        for (auto& pair : node->children) {
            deleteTrie(pair.second);
        }
        delete node;
    }
};

class Solution {
public:
    // Подход 1: DFS с мемоизацией и Trie (Наиболее оптимальный)
    // Время: O(n * 2^n) в худшем случае, Память: O(n * 2^n)
    vector<string> wordBreak(string s, vector<string>& wordDict) {
        /*
        Используем Trie для эффективного поиска слов и DFS с мемоизацией
        для построения всех возможных предложений.
        */
        // Строим Trie из словаря
        Trie trie;
        for (const string& word : wordDict) {
            trie.insert(word);
        }
        
        // Словарь для мемоизации
        unordered_map<int, vector<string>> memo;
        
        return dfs(s, 0, trie, memo);
    }
    
private:
    vector<string> dfs(const string& s, int start, Trie& trie, 
                      unordered_map<int, vector<string>>& memo) {
        // Если достигли конца строки
        if (start == s.length()) {
            return {""};
        }
        
        // Если результат уже вычислен
        if (memo.find(start) != memo.end()) {
            return memo[start];
        }
        
        vector<string> results;
        
        // Пробуем все возможные слова
        for (int end = start + 1; end <= s.length(); ++end) {
            string word = s.substr(start, end - start);
            
            if (trie.search(word)) {
                vector<string> subResults = dfs(s, end, trie, memo);
                
                for (const string& sub : subResults) {
                    if (sub.empty()) {
                        results.push_back(word);
                    } else {
                        results.push_back(word + " " + sub);
                    }
                }
            }
        }
        
        memo[start] = results;
        return results;
    }

public:
    // Подход 2: DFS с мемоизацией (без Trie)
    // Время: O(n * 2^n), Память: O(n * 2^n)
    vector<string> wordBreak_simple(string s, vector<string>& wordDict) {
        /*
        Простой подход с использованием множества для словаря.
        */
        unordered_set<string> wordSet(wordDict.begin(), wordDict.end());
        unordered_map<int, vector<string>> memo;
        
        return dfsSimple(s, 0, wordSet, memo);
    }
    
private:
    vector<string> dfsSimple(const string& s, int start,
                            unordered_set<string>& wordSet,
                            unordered_map<int, vector<string>>& memo) {
        if (start == s.length()) {
            return {""};
        }
        
        if (memo.find(start) != memo.end()) {
            return memo[start];
        }
        
        vector<string> results;
        
        for (int end = start + 1; end <= s.length(); ++end) {
            string word = s.substr(start, end - start);
            
            if (wordSet.count(word)) {
                vector<string> subResults = dfsSimple(s, end, wordSet, memo);
                
                for (const string& sub : subResults) {
                    if (sub.empty()) {
                        results.push_back(word);
                    } else {
                        results.push_back(word + " " + sub);
                    }
                }
            }
        }
        
        memo[start] = results;
        return results;
    }
};