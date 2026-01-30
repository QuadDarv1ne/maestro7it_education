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

#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <climits>

using namespace std;

class Solution {
private:
    struct TrieNode {
        unordered_map<char, TrieNode*> children;
        vector<int> ids;
        
        ~TrieNode() {
            for (auto& p : children) {
                delete p.second;
            }
        }
    };
    
    TrieNode* buildTrie(const unordered_set<string>& strings, 
                        const unordered_map<string, int>& strToId) {
        TrieNode* root = new TrieNode();
        for (const string& s : strings) {
            TrieNode* node = root;
            for (char ch : s) {
                if (node->children.find(ch) == node->children.end()) {
                    node->children[ch] = new TrieNode();
                }
                node = node->children[ch];
            }
            node->ids.push_back(strToId.at(s));
        }
        return root;
    }
    
    vector<pair<int, int>> findMatches(TrieNode* trie, const string& s, int start) {
        vector<pair<int, int>> matches;
        TrieNode* node = trie;
        int pos = start;
        
        while (pos < s.length() && node->children.find(s[pos]) != node->children.end()) {
            node = node->children[s[pos]];
            pos++;
            if (!node->ids.empty()) {
                for (int id : node->ids) {
                    matches.push_back({pos - start, id});
                }
            }
        }
        return matches;
    }
    
public:
    long long minimumCost(string source, string target, vector<string>& original, 
                          vector<string>& changed, vector<int>& cost) {
        // Создание уникальных ID для строк
        unordered_set<string> unique;
        for (const string& s : original) unique.insert(s);
        for (const string& s : changed) unique.insert(s);
        
        unordered_map<string, int> strToId;
        int idx = 0;
        for (const string& s : unique) {
            strToId[s] = idx++;
        }
        
        int n = unique.size();
        const long long INF = LLONG_MAX / 2;
        
        // Матрица расстояний
        vector<vector<long long>> dist(n, vector<long long>(n, INF));
        for (int i = 0; i < n; i++) {
            dist[i][i] = 0;
        }
        
        for (int i = 0; i < original.size(); i++) {
            int sid = strToId[original[i]];
            int tid = strToId[changed[i]];
            dist[sid][tid] = min(dist[sid][tid], (long long)cost[i]);
        }
        
        // Floyd-Warshall
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                if (dist[i][k] < INF) {
                    for (int j = 0; j < n; j++) {
                        if (dist[k][j] < INF) {
                            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
                        }
                    }
                }
            }
        }
        
        // Построение Trie
        TrieNode* srcTrie = buildTrie(unique, strToId);
        TrieNode* tgtTrie = buildTrie(unique, strToId);
        
        // DP
        int m = source.length();
        vector<long long> dp(m + 1, INF);
        dp[m] = 0;
        
        for (int i = m - 1; i >= 0; i--) {
            if (source[i] == target[i] && dp[i + 1] < INF) {
                dp[i] = dp[i + 1];
            }
            
            auto srcMatches = findMatches(srcTrie, source, i);
            auto tgtMatches = findMatches(tgtTrie, target, i);
            
            unordered_map<int, vector<int>> tgtByLen;
            for (auto& p : tgtMatches) {
                tgtByLen[p.first].push_back(p.second);
            }
            
            for (auto& srcPair : srcMatches) {
                int srcLen = srcPair.first;
                int sid = srcPair.second;
                
                if (tgtByLen.find(srcLen) != tgtByLen.end() && dp[i + srcLen] < INF) {
                    for (int tid : tgtByLen[srcLen]) {
                        if (dist[sid][tid] < INF) {
                            dp[i] = min(dp[i], dist[sid][tid] + dp[i + srcLen]);
                        }
                    }
                }
            }
        }
        
        delete srcTrie;
        delete tgtTrie;
        
        return dp[0] < INF ? dp[0] : -1;
    }
};