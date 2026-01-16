"""
Поиск всех путей от корня к листьям с заданной суммой

@param root: Корень бинарного дерева
@param targetSum: Целевая сумма значений узлов в пути  
@return: Список всех путей, удовлетворяющих условию

Сложность: Время O(N), Память O(H) для рекурсии + O(N) для путей

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

class Solution(object):
    def pathSum(self, root, targetSum):
        """
        :type root: TreeNode
        :type targetSum: int
        :rtype: List[List[int]]
        """
        result = []
        
        def dfs(node, current_sum, path):
            if not node:
                return
            
            # Добавляем текущий узел в путь
            path.append(node.val)
            
            # Проверяем, является ли узел листом с нужной суммой
            if not node.left and not node.right and current_sum + node.val == targetSum:
                # Используем срез [:] для создания копии списка (работает в Python 2 и 3)
                result.append(path[:])
            
            # Рекурсивно обходим левое и правое поддеревья
            dfs(node.left, current_sum + node.val, path)
            dfs(node.right, current_sum + node.val, path)
            
            # Backtracking: удаляем текущий узел из пути
            path.pop()
        
        dfs(root, 0, [])
        return result


# Определение класса TreeNode для тестирования
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right