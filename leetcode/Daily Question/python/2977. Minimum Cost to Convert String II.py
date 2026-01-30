"""
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
"""


class Solution:
    def minimumCost(self, source, target, original, changed, cost):
        """
        Находит минимальную стоимость преобразования строки source в target
        
        Аргументы:
            source: исходная строка
            target: целевая строка
            original: список исходных подстрок для замены
            changed: список целевых подстрок для замены
            cost: список стоимостей преобразований
            
        Возвращает:
            Минимальная стоимость преобразования или -1, если невозможно
        """
        # Создание уникальных ID для строк
        unique = set(original + changed)
        str_to_id = {s: i for i, s in enumerate(unique)}
        n = len(unique)
        
        # Матрица расстояний Floyd-Warshall
        INF = float('inf')
        dist = [[INF] * n for _ in range(n)]
        
        for i in range(n):
            dist[i][i] = 0
        
        for i in range(len(original)):
            sid = str_to_id[original[i]]
            tid = str_to_id[changed[i]]
            dist[sid][tid] = min(dist[sid][tid], cost[i])
        
        # Floyd-Warshall
        for k in range(n):
            for i in range(n):
                if dist[i][k] < INF:
                    for j in range(n):
                        if dist[k][j] < INF:
                            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        
        # Построение Trie для быстрого поиска
        class TrieNode:
            def __init__(self):
                self.children = {}
                self.ids = []
        
        def build_trie(strings):
            root = TrieNode()
            for s in strings:
                node = root
                for ch in s:
                    if ch not in node.children:
                        node.children[ch] = TrieNode()
                    node = node.children[ch]
                node.ids.append(str_to_id[s])
            return root
        
        src_trie = build_trie(unique)
        tgt_trie = build_trie(unique)
        
        # Поиск всех совпадающих подстрок от позиции
        def find_matches(trie, s, start):
            matches = []
            node = trie
            pos = start
            while pos < len(s) and s[pos] in node.children:
                node = node.children[s[pos]]
                pos += 1
                if node.ids:
                    for sid in node.ids:
                        matches.append((pos - start, sid))
            return matches
        
        # DP с мемоизацией
        m = len(source)
        dp = [INF] * (m + 1)
        dp[m] = 0
        
        for i in range(m - 1, -1, -1):
            # Символы совпадают
            if source[i] == target[i] and dp[i + 1] < INF:
                dp[i] = dp[i + 1]
            
            # Поиск подстрок
            src_matches = find_matches(src_trie, source, i)
            tgt_matches = find_matches(tgt_trie, target, i)
            
            # Группировка по длине для оптимизации
            tgt_by_len = {}
            for length, tid in tgt_matches:
                if length not in tgt_by_len:
                    tgt_by_len[length] = []
                tgt_by_len[length].append(tid)
            
            for src_len, sid in src_matches:
                if src_len in tgt_by_len and dp[i + src_len] < INF:
                    for tid in tgt_by_len[src_len]:
                        if dist[sid][tid] < INF:
                            dp[i] = min(dp[i], dist[sid][tid] + dp[i + src_len])
        
        return dp[0] if dp[0] < INF else -1