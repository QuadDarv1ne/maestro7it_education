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

class Solution {
public:
    long long countPalindromePaths(vector<int>& parent, string s) {
        int n = parent.size();
        vector<vector<int>> tree(n);
        for (int i = 1; i < n; i++) {
            tree[parent[i]].push_back(i);
        }
        
        long long ans = 0;
        unordered_map<int, int> maskCount;
        
        function<void(int, int)> dfs = [&](int node, int mask) {
            ans += maskCount[mask];
            for (int i = 0; i < 26; i++) {
                ans += maskCount[mask ^ (1 << i)];
            }
            
            maskCount[mask]++;
            
            for (int child : tree[node]) {
                int childMask = mask ^ (1 << (s[child] - 'a'));
                dfs(child, childMask);
            }
        };
        
        dfs(0, 0);
        return ans;
    }
};