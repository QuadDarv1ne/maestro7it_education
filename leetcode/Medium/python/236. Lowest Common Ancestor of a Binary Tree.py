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
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root, p, q):
        """
        Находит наименьшего общего предка двух узлов в бинарном дереве.
        
        Алгоритм (рекурсивный поиск):
        1. Если текущий узел равен p или q, возвращаем текущий узел.
        2. Рекурсивно ищем p и q в левом и правом поддеревьях.
        3. Если оба поддерева вернули не-None узлы, то текущий узел - LCA.
        4. Иначе возвращаем то, что не None (или None, если оба None).
        
        Сложность:
        Время: O(n), где n - количество узлов в дереве (в худшем случае)
        Пространство: O(h), где h - высота дерева (глубина рекурсии)
        
        Параметры:
        ----------
        root : TreeNode
            Корень бинарного дерева
        p : TreeNode
            Первый узел
        q : TreeNode
            Второй узел
            
        Возвращает:
        -----------
        TreeNode
            Наименьший общий предок узлов p и q
            
        Пример:
        -------
        Входное дерево:
               3
             /   \
            5     1
           / \   / \
          6   2 0   8
             / \
            7   4
        
        p = 5, q = 1 → LCA = 3
        p = 5, q = 4 → LCA = 5
        """
        if not root:
            return None
        
        # Если текущий узел равен p или q, возвращаем его
        if root == p or root == q:
            return root
        
        # Рекурсивно ищем в левом и правом поддеревьях
        left_lca = self.lowestCommonAncestor(root.left, p, q)
        right_lca = self.lowestCommonAncestor(root.right, p, q)
        
        # Если оба поддерева вернули не-None, то текущий узел - LCA
        if left_lca and right_lca:
            return root
        
        # Иначе возвращаем то, что не None
        return left_lca if left_lca else right_lca
    
    def lowestCommonAncestor_iterative(self, root, p, q):
        """
        Итеративное решение с использованием стека и родительских указателей.
        
        Алгоритм:
        1. Используем стек для обхода дерева.
        2. Строим словарь родительских указателей для каждого узла.
        3. Находим пути от p и q к корню.
        4. Находим пересечение путей - это и будет LCA.
        
        Сложность:
        Время: O(n)
        Пространство: O(n) для хранения родительских указателей
        """
        if not root:
            return None
        
        # Стек для обхода дерева
        stack = [root]
        # Словарь для хранения родительских указателей
        parent = {root: None}
        
        # Обходим дерево, пока не найдем оба узла
        while p not in parent or q not in parent:
            node = stack.pop()
            
            if node.left:
                parent[node.left] = node
                stack.append(node.left)
            if node.right:
                parent[node.right] = node
                stack.append(node.right)
        
        # Находим всех предков узла p
        ancestors = set()
        while p:
            ancestors.add(p)
            p = parent[p]
        
        # Находим первого общего предка узла q
        while q not in ancestors:
            q = parent[q]
        
        return q