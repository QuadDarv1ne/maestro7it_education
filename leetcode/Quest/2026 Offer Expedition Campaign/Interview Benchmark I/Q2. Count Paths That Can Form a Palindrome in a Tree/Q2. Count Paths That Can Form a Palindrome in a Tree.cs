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

public class Solution {
    private List<int>[] tree;
    private string s;
    private long ans = 0;
    private Dictionary<int, int> maskCount = new Dictionary<int, int>();
    
    public long CountPalindromePaths(IList<int> parent, string s) {
        int n = parent.Count;
        this.s = s;
        tree = new List<int>[n];
        for (int i = 0; i < n; i++) tree[i] = new List<int>();
        for (int i = 1; i < n; i++) {
            tree[parent[i]].Add(i);
        }
        
        Dfs(0, 0);
        return ans;
    }
    
    private void Dfs(int node, int mask) {
        maskCount.TryGetValue(mask, out int count);
        ans += count;
        for (int i = 0; i < 26; i++) {
            maskCount.TryGetValue(mask ^ (1 << i), out count);
            ans += count;
        }
        
        maskCount[mask] = maskCount.GetValueOrDefault(mask) + 1;
        
        foreach (int child in tree[node]) {
            int childMask = mask ^ (1 << (s[child] - 'a'));
            Dfs(child, childMask);
        }
    }
}