class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid):
        """
        Автор: Дуплей Максим Игоревич
        ORCID: https://orcid.org/0009-0007-7605-539X
        GitHub: https://github.com/QuadDarv1ne/
        
        Задача: Unique Paths II (LeetCode)
        Алгоритм: Динамическое программирование для подсчета путей с препятствиями
        Сложность: O(m * n) по времени, O(m * n) по памяти
        
        Идея решения:
        1. Создаем DP таблицу для хранения количества путей к каждой клетке
        2. Если клетка содержит препятствие - путей к ней 0
        3. Иначе: количество путей = пути сверху + пути слева
        4. dp[i][j] = dp[i-1][j] + dp[i][j-1]
        """
        
        # Если старт или финиш заблокированы
        if obstacleGrid[0][0] == 1:
            return 0
        
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])
        
        # Создаем DP таблицу
        dp = [[0] * n for _ in range(m)]
        dp[0][0] = 1  # Стартовая позиция
        
        # Заполняем DP таблицу
        for i in range(m):
            for j in range(n):
                # Пропускаем стартовую позицию
                if i == 0 and j == 0:
                    continue
                
                # Если текущая клетка - препятствие
                if obstacleGrid[i][j] == 1:
                    dp[i][j] = 0
                else:
                    # Суммируем пути сверху и слева
                    from_top = dp[i-1][j] if i > 0 else 0
                    from_left = dp[i][j-1] if j > 0 else 0
                    dp[i][j] = from_top + from_left
        
        return dp[m-1][n-1]


"""
Полезные ссылки автора:
Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
Telegram: @quadd4rv1n7, @dupley_maxim_1999
Rutube: https://rutube.ru/channel/4218729/
Plvideo: https://plvideo.ru/channel/AUPv_p1r5AQJ
YouTube: https://www.youtube.com/@it-coders
VK: https://vk.com/science_geeks
"""