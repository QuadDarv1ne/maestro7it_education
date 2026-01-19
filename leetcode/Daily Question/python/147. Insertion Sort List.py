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

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    """
    @brief Сортирует связный список с использованием алгоритма сортировки вставками
    
    Алгоритм сортировки вставками для связного списка:
    1. Создаем фиктивный узел для нового отсортированного списка
    2. Итеративно вставляем каждый узел исходного списка в правильную позицию
    3. Для каждого узла находим позицию в отсортированном списке, где он должен находиться
    
    Сложность: O(n²) время в худшем случае, O(1) память
    
    @param head: Голова несортированного списка
    @return: Голова отсортированного списка
    """
    def insertionSortList(self, head):
        if not head or not head.next:
            return head
        
        # Создаем фиктивный узел для нового отсортированного списка
        dummy = ListNode(0)
        curr = head
        
        while curr:
            # Сохраняем следующий узел
            next_node = curr.next
            prev = dummy
            
            # Находим позицию для вставки в отсортированном списке
            while prev.next and prev.next.val < curr.val:
                prev = prev.next
            
            # Вставляем curr между prev и prev.next
            curr.next = prev.next
            prev.next = curr
            
            # Переходим к следующему узлу в исходном списке
            curr = next_node
        
        return dummy.next