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
    private List<Integer>[] tree;
    private String s;
    private long ans = 0;
    private Map<Integer, Integer> maskCount = new HashMap<>();
    
    public long countPalindromePaths(List<Integer> parent, String s) {
        int n = parent.size();
        this.s = s;
        tree = new ArrayList[n];
        for (int i = 0; i < n; i++) tree[i] = new ArrayList<>();
        for (int i = 1; i < n; i++) {
            tree[parent.get(i)].add(i);
        }
        
        dfs(0, 0);
        return ans;
    }
    
    private void dfs(int node, int mask) {
        ans += maskCount.getOrDefault(mask, 0);
        for (int i = 0; i < 26; i++) {
            ans += maskCount.getOrDefault(mask ^ (1 << i), 0);
        }
        
        maskCount.put(mask, maskCount.getOrDefault(mask, 0) + 1);
        
        for (int child : tree[node]) {
            int childMask = mask ^ (1 << (s.charAt(child) - 'a'));
            dfs(child, childMask);
        }
    }
}