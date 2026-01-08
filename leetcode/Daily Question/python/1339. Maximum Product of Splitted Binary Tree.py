"""
Максимальное произведение разделенного бинарного дерева

@param root Корень бинарного дерева
@return Максимальное произведение сумм двух поддеревьев по модулю 10^9 + 7

Сложность: Время O(n), Память O(h), где n - количество узлов, h - высота дерева

Автор: Дуплей Максим Игоревич
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
    def maxProduct(self, root):
        MOD = 10**9 + 7
        
        # Шаг 1: Вычисление общей суммы всех узлов дерева
        def calculate_total(node):
            if not node:
                return 0
            return node.val + calculate_total(node.left) + calculate_total(node.right)
        
        total_sum = calculate_total(root)
        self.max_product = 0
        
        # Шаг 2: DFS для вычисления сумм поддеревьев и поиска максимального произведения
        def dfs(node):
            if not node:
                return 0
            
            # Вычисление суммы текущего поддерева (постфиксный обход)
            left_sum = dfs(node.left)
            right_sum = dfs(node.right)
            subtree_sum = node.val + left_sum + right_sum
            
            # Если удалить ребро над текущим узлом, получим:
            # - Одно поддерево с суммой = subtree_sum
            # - Другое поддерево с суммой = total_sum - subtree_sum
            product = subtree_sum * (total_sum - subtree_sum)
            self.max_product = max(self.max_product, product)
            
            return subtree_sum
        
        dfs(root)
        return self.max_product % MOD