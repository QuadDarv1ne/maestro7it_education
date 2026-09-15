'''
https://leetcode.com/problems/permutation-sequence/description/
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

class Solution:
    def pathsWithMaxScore(self, board):
        """
        Находит максимальный счет и количество путей с этим счетом.
        
        Игрок начинает с позиции (n-1, n-1) и движется вверх, влево или по диагонали
        к позиции (0, 0). Цифры на пути добавляются к счету. Символы 'E' и 'S' 
        не добавляют очков. Препятствия 'X' блокируют путь.
        
        Args:
            board: Список строк, представляющих игровое поле
            
        Returns:
            Список из двух чисел [max_score, count]:
            - max_score: максимально возможный счет, или 0 если пути нет
            - count: количество путей с максимальным счетом по модулю 10^9+7
        """
        MOD = 10**9 + 7
        n = len(board)
        
        # dp[i][j] = [max_score, count]
        dp = [[[-1, 0] for _ in range(n)] for _ in range(n)]
        
        # Начальная позиция
        dp[n-1][n-1] = [0, 1]
        
        # Заполняем dp снизу вверх и справа налево
        for i in range(n-1, -1, -1):
            for j in range(n-1, -1, -1):
                if board[i][j] == 'X' or (i == n-1 and j == n-1):
                    continue
                
                max_score = -1
                count = 0
                
                # Проверяем три возможных направления
                directions = [(1, 0), (0, 1), (1, 1)]  # вниз, вправо, диагональ
                
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < n and dp[ni][nj][0] != -1:
                        score = dp[ni][nj][0]
                        if score > max_score:
                            max_score = score
                            count = dp[ni][nj][1]
                        elif score == max_score:
                            count = (count + dp[ni][nj][1]) % MOD
                
                if max_score != -1:
                    # Добавляем очки текущей клетки (если это не 'E' и не 'S')
                    if board[i][j] != 'E' and board[i][j] != 'S':
                        max_score += int(board[i][j])
                    dp[i][j] = [max_score, count]
        
        if dp[0][0][0] == -1:
            return [0, 0]
        return [dp[0][0][0], dp[0][0][1]]