'''
https://leetcode.com/problems/maximum-number-of-k-divisible-components/description/?envType=daily-question&envId=2025-11-28
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Maximum Number of K-Divisible Components"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

class Solution:
    def maxKDivisibleComponents(self, n: int, edges: List[List[int]], values: List[int], k: int) -> int:
        # Строим граф
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        self.components = 0
        
        def dfs(node: int, parent: int) -> int:
            # Начинаем с значения текущего узла
            total = values[node]
            
            # Обрабатываем всех соседей кроме родителя
            for neighbor in graph[node]:
                if neighbor != parent:
                    total += dfs(neighbor, node)
            
            # Если сумма делится на k, увеличиваем счетчик компонент
            if total % k == 0:
                self.components += 1
            
            return total
        
        # Запускаем DFS из корня (узла 0)
        dfs(0, -1)
        return self.components