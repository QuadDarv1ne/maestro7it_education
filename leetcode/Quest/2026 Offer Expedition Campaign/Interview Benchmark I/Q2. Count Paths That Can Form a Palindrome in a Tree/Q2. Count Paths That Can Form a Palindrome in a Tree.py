'''
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
'''

from collections import defaultdict

class Solution:
    def countPalindromePaths(self, parent, s):
        n = len(parent)
        tree = defaultdict(list)
        for i in range(1, n):
            tree[parent[i]].append(i)
        
        self.ans = 0
        mask_count = defaultdict(int)
        
        def dfs(node, mask):
            # Count pairs with previously seen nodes
            self.ans += mask_count[mask]
            for i in range(26):
                self.ans += mask_count[mask ^ (1 << i)]
            
            mask_count[mask] += 1
            
            for child in tree[node]:
                child_mask = mask ^ (1 << (ord(s[child]) - ord('a')))
                dfs(child, child_mask)
        
        dfs(0, 0)
        return self.ans