'''
https://leetcode.com/problems/balance-a-binary-search-tree/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "1382. Balance a Binary Search Tree"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def balanceBST(self, root):
        """
        Балансирует бинарное дерево поиска (BST).
        
        Алгоритм:
        1. Выполняет симметричный обход (in-order) BST для получения отсортированного списка значений.
        2. Рекурсивно строит сбалансированное BST из отсортированного списка,
           выбирая средний элемент в качестве корня для каждого поддерева.
        
        Параметры:
        ----------
        root : TreeNode
            Корень исходного BST, который может быть несбалансированным.
            
        Возвращает:
        -----------
        TreeNode
            Корень нового сбалансированного BST.
            
        Сложность:
        ----------
        Время: O(n), где n - количество узлов в дереве.
        Пространство: O(n) для хранения отсортированных значений.
        
        Пример:
        -------
        Входное дерево:
            1
             \\
              2
               \\
                3
                 \\
                  4
        
        Выходное дерево:
              2
             / \\
            1   3
                 \\
                  4
        """
        
        # Шаг 1: Симметричный обход для получения отсортированных значений
        sorted_values = []
        
        def inorder(node):
            """
            Рекурсивно выполняет симметричный обход дерева.
            
            Параметры:
            ----------
            node : TreeNode
                Текущий узел для обработки.
            """
            if not node:
                return
            inorder(node.left)
            sorted_values.append(node.val)
            inorder(node.right)
        
        inorder(root)
        
        # Шаг 2: Построение сбалансированного BST из отсортированных значений
        def buildBalancedBST(left, right):
            """
            Рекурсивно строит сбалансированное BST из отсортированного массива.
            
            Параметры:
            ----------
            left : int
                Левая граница текущего подмассива.
            right : int
                Правая граница текущего подмассива.
                
            Возвращает:
            -----------
            TreeNode
                Корень сбалансированного поддерева.
            """
            if left > right:
                return None
            
            # Средний элемент становится корнем для сбалансированного дерева
            mid = (left + right) // 2
            node = TreeNode(sorted_values[mid])
            
            # Рекурсивно строим левое и правое поддеревья
            node.left = buildBalancedBST(left, mid - 1)
            node.right = buildBalancedBST(mid + 1, right)
            
            return node
        
        return buildBalancedBST(0, len(sorted_values) - 1)