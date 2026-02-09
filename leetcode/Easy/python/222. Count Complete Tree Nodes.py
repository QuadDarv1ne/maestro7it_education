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
    def countNodes(self, root):
        """
        Подсчитывает количество узлов в полном бинарном дереве.
        
        Алгоритм:
        1. Находим высоту дерева по левому и правому краям.
        2. Если высоты равны, дерево идеальное (perfect) и количество узлов = 2^h - 1.
        3. Если высоты разные, рекурсивно считаем для левого и правого поддеревьев.
        
        Сложность:
        Время: O(log² n), где n - количество узлов
        Пространство: O(log n) для рекурсивного стека
        
        Параметры:
        ----------
        root : TreeNode
            Корень полного бинарного дерева
            
        Возвращает:
        -----------
        int
            Количество узлов в дереве
            
        Пример:
        -------
        Вход: [1,2,3,4,5,6]
        Выход: 6
        """
        if not root:
            return 0
        
        # Вычисляем высоты по левому и правому краям
        left_height = self._get_height(root, 'left')
        right_height = self._get_height(root, 'right')
        
        # Если дерево идеальное (perfect)
        if left_height == right_height:
            return (1 << left_height) - 1  # 2^h - 1
        
        # Если дерево не идеальное, рекурсивно считаем оба поддерева
        return 1 + self.countNodes(root.left) + self.countNodes(root.right)
    
    def _get_height(self, node, direction):
        """
        Вычисляет высоту дерева, идя только по указанному направлению.
        
        Параметры:
        ----------
        node : TreeNode
            Начальный узел
        direction : str
            Направление: 'left' для левого края, 'right' для правого края
            
        Возвращает:
        -----------
        int
            Высота дерева по указанному направлению
        """
        height = 0
        while node:
            height += 1
            node = node.left if direction == 'left' else node.right
        return height