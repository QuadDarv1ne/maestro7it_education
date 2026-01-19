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
    """
    @brief Выполняет последующий обход (postorder) бинарного дерева
    
    Последующий обход (postorder traversal):
    1. Обходим левое поддерево
    2. Обходим правое поддерево
    3. Посещаем корень
    
    @param root: Корень бинарного дерева
    @return: Список значений узлов в порядке postorder
    """
    def postorderTraversal(self, root):
        result = []
        self._postorder_recursive(root, result)
        return result
    
    def _postorder_recursive(self, node, result):
        """Рекурсивная вспомогательная функция"""
        if node is None:
            return
        
        self._postorder_recursive(node.left, result)  # Обходим левое поддерево
        self._postorder_recursive(node.right, result) # Обходим правое поддерево
        result.append(node.val)                      # Посещаем корень