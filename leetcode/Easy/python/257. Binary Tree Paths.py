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

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def binaryTreePaths(self, root):
        """
        Возвращает все пути от корня до листьев в бинарном дереве.
        
        Алгоритм (рекурсивный DFS):
        1. Если узел пустой, возвращаем пустой список.
        2. Если узел - лист (нет левого и правого потомков), добавляем путь к результату.
        3. Рекурсивно обходим левое и правое поддеревья, добавляя текущий узел к пути.
        
        Сложность:
        Время: O(n), где n - количество узлов в дереве (посещаем каждый узел один раз)
        Пространство: O(h) для рекурсивного стека, где h - высота дерева
        
        Параметры:
        ----------
        root : TreeNode
            Корень бинарного дерева
            
        Возвращает:
        -----------
        List[str]
            Список строк, представляющих пути от корня до листьев
            
        Примеры:
        --------
        Входное дерево:
              1
            /   \\
           2     3
            \\
             5
        
        Выход: ["1->2->5", "1->3"]
        """
        def dfs(node, path):
            """
            Рекурсивный обход дерева в глубину.
            
            Параметры:
            ----------
            node : TreeNode
                Текущий узел
            path : str
                Текущий путь от корня до данного узла
            """
            if not node:
                return
            
            # Добавляем текущий узел к пути
            if not path:
                current_path = str(node.val)
            else:
                current_path = path + "->" + str(node.val)
            
            # Если узел - лист (нет потомков), добавляем путь к результату
            if not node.left and not node.right:
                result.append(current_path)
                return
            
            # Рекурсивно обходим левое и правое поддеревья
            if node.left:
                dfs(node.left, current_path)
            if node.right:
                dfs(node.right, current_path)
        
        result = []
        if root:
            dfs(root, "")
        return result
    
    def binaryTreePaths_iterative(self, root):
        """
        Итеративное решение с использованием стека (DFS).
        
        Алгоритм:
        1. Используем стек для хранения пар (узел, текущий путь)
        2. Пока стек не пуст:
           - Извлекаем узел и путь
           - Если узел - лист, добавляем путь к результату
           - Добавляем потомков в стек с обновленным путем
        
        Сложность:
        Время: O(n)
        Пространство: O(n) для стека
        """
        if not root:
            return []
        
        result = []
        stack = [(root, "")]
        
        while stack:
            node, path = stack.pop()
            
            # Обновляем путь для текущего узла
            if not path:
                current_path = str(node.val)
            else:
                current_path = path + "->" + str(node.val)
            
            # Если узел - лист, добавляем путь к результату
            if not node.left and not node.right:
                result.append(current_path)
            
            # Добавляем потомков в стек (сначала правый, потом левый для порядка)
            if node.right:
                stack.append((node.right, current_path))
            if node.left:
                stack.append((node.left, current_path))
        
        return result
    
    def binaryTreePaths_bfs(self, root):
        """
        Решение с использованием очереди (BFS).
        
        Алгоритм:
        1. Используем очередь для обхода дерева по уровням
        2. Храним в очереди пары (узел, текущий путь)
        3. При достижении листа добавляем путь к результату
        
        Сложность:
        Время: O(n)
        Пространство: O(n) для очереди
        """
        if not root:
            return []
        
        from collections import deque
        
        result = []
        queue = deque([(root, "")])
        
        while queue:
            node, path = queue.popleft()
            
            # Обновляем путь для текущего узла
            if not path:
                current_path = str(node.val)
            else:
                current_path = path + "->" + str(node.val)
            
            # Если узел - лист, добавляем путь к результату
            if not node.left and not node.right:
                result.append(current_path)
            
            # Добавляем потомков в очередь
            if node.left:
                queue.append((node.left, current_path))
            if node.right:
                queue.append((node.right, current_path))
        
        return result