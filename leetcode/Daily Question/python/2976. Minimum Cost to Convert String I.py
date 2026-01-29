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
        INF = float('inf')
        # Создаем матрицу 26x26 для преобразований символов
        dist = [[INF] * 26 for _ in range(26)]
        
        # Инициализация: преобразование символа в себя стоит 0
        for i in range(26):
            dist[i][i] = 0
        
        # Добавляем заданные преобразования (берем минимальную стоимость, если несколько путей)
        for i in range(len(original)):
            u = ord(original[i]) - ord('a')
            v = ord(changed[i]) - ord('a')
            dist[u][v] = min(dist[u][v], cost[i])
        
        # Алгоритм Флойда-Уоршелла для поиска кратчайших путей между всеми парами
        for k in range(26):
            for i in range(26):
                if dist[i][k] == INF:
                    continue
                for j in range(26):
                    if dist[k][j] == INF:
                        continue
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        
        # Вычисляем общую стоимость преобразования source в target
        total = 0
        for i in range(len(source)):
            u = ord(source[i]) - ord('a')
            v = ord(target[i]) - ord('a')
            
            # Если преобразование невозможно
            if dist[u][v] == INF:
                return -1
            total += dist[u][v]
        
        return total