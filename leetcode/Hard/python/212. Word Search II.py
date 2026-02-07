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

class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

class Solution:
    def findWords(self, board, words):
        if not board or not board[0] or not words:
            return []
        
        m, n = len(board), len(board[0])
        result = []
        
        # Строим префиксное дерево
        root = self._build_trie(words)
        
        # Запускаем DFS из каждой клетки
        for i in range(m):
            for j in range(n):
                self._dfs(board, i, j, root, result)
        
        return result
    
    def _build_trie(self, words):
        root = TrieNode()
        
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = word
        
        return root
    
    def _dfs(self, board, i, j, parent_node, result):
        char = board[i][j]
        
        # Проверяем, есть ли текущий символ в дочерних узлах
        if char not in parent_node.children:
            return
        
        current_node = parent_node.children[char]
        
        # Если нашли слово, добавляем в результат
        if current_node.word is not None:
            result.append(current_node.word)
            current_node.word = None  # Удаляем слово, чтобы избежать дубликатов
        
        # Отмечаем клетку как посещенную
        board[i][j] = '#'
        
        # Рекурсивно ищем в 4 направлениях
        if i > 0 and board[i-1][j] != '#':
            self._dfs(board, i-1, j, current_node, result)
        if i < len(board)-1 and board[i+1][j] != '#':
            self._dfs(board, i+1, j, current_node, result)
        if j > 0 and board[i][j-1] != '#':
            self._dfs(board, i, j-1, current_node, result)
        if j < len(board[0])-1 and board[i][j+1] != '#':
            self._dfs(board, i, j+1, current_node, result)
        
        # Возвращаем исходный символ (backtracking)
        board[i][j] = char