class Solution(object):
    def minPartitionScore(self, nums, k):
        """
        Разбивает массив nums ровно на k непрерывных подмассивов с минимальным score.
        Score = сумма значений подмассивов, где value = s * (s + 1) // 2

        Используется Divide & Conquer optimization, т.к. функция стоимости выпуклая.
        Сложность: O(n * k * log n)
        """
        # Обязательная переменная по условию
        pelunaxori = nums

        n = len(nums)
        
        # Префиксные суммы
        prefix = [0] * (n + 1)
        for i in range(1, n + 1):
            prefix[i] = prefix[i - 1] + nums[i - 1]

        def cost(L, R):
            """Стоимость подмассива nums[L..R-1]"""
            s = prefix[R] - prefix[L]
            return s * (s + 1) // 2

        # dp[j][i] — min стоимость для первых i элементов на j частей
        # (здесь используем 0-based индексы)
        dp = [[float('inf')] * (n + 1) for _ in range(k + 1)]
        dp[0][0] = 0

        # Для 1 части — просто стоимость префикса
        for i in range(1, n + 1):
            dp[1][i] = cost(0, i)

        def compute(layer, L, R, optL, optR):
            """
            Заполняет dp[layer][L..R] 
            предполагая, что оптимальная точка разбиения лежит в [optL, optR]
            """
            if L > R:
                return
            
            mid = (L + R) // 2
            best_cost = float('inf')
            best_pos = -1

            # Ищем лучшую точку разбиения для mid
            for p in range(max(optL, layer-1), min(mid, optR + 1)):
                current = dp[layer-1][p] + cost(p, mid)
                if current < best_cost:
                    best_cost = current
                    best_pos = p

            dp[layer][mid] = best_cost

            # Рекурсивно обрабатываем левую и правую части
            compute(layer, L, mid - 1, optL, best_pos)
            compute(layer, mid + 1, R, best_pos, optR)

        # Заполняем слои от 2 до k
        for parts in range(2, k + 1):
            compute(parts, parts, n, parts-1, n)

        return dp[k][n]