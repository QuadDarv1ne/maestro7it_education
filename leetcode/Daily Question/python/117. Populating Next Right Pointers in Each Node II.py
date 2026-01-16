"""
Соединение узлов произвольного бинарного дерева с правыми соседями

@param root: Корень бинарного дерева
@return: Модифицированное дерево с установленными next-указателями

Сложность: Время O(N), Память O(1)

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

# class Node:
#     def __init__(self, val=0, left=None, right=None, next=None):
#         self.val = val
#         self.left = left
#         self.right = right
#         self.next = next

class Solution:
    def connect(self, root):
        """
        :type root: Node
        :rtype: Node
        """
        if not root:
            return root
        
        curr = root
        
        while curr:
            # Dummy-узел для начала нового уровня
            dummy = Node(0)
            tail = dummy
            
            # Проходим по текущему уровню
            while curr:
                # Подсоединяем левого ребенка, если есть
                if curr.left:
                    tail.next = curr.left
                    tail = tail.next
                
                # Подсоединяем правого ребенка, если есть
                if curr.right:
                    tail.next = curr.right
                    tail = tail.next
                
                # Переходим к следующему узлу на текущем уровне
                curr = curr.next
            
            # Переходим на следующий уровень
            curr = dummy.next
        
        return root