'''
LeetCode 79. Word Search
https://leetcode.com/problems/word-search/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. YouTube канал: https://www.youtube.com/@it-coders
6. ВК группа: https://vk.com/science_geeks
'''

# ========================== PYTHON ==========================

class Solution:
    def exist(self, board, word):
        m, n = len(board), len(board[0])
        
        def dfs(i, j, idx):
            if idx == len(word):
                return True
            if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[idx]:
                return False
            
            temp = board[i][j]
            board[i][j] = '#'  # Помечаем как посещённую
            
            found = (dfs(i + 1, j, idx + 1) or dfs(i - 1, j, idx + 1) or
                     dfs(i, j + 1, idx + 1) or dfs(i, j - 1, idx + 1))
            
            board[i][j] = temp  # Восстанавливаем
            return found
        
        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False