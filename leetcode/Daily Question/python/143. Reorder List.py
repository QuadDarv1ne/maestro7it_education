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
    @brief Переупорядочивает связный список в порядке L0→Ln→L1→Ln-1→L2→Ln-2→...
    
    Алгоритм:
    1. Находим середину списка с помощью быстрого и медленного указателей
    2. Разделяем список на две половины
    3. Реверсируем вторую половину
    4. Сливаем две половины, чередуя узлы
    
    @param head: Голова связного списка
    @return: None (изменяет список на месте)
    """
    def reorderList(self, head):
        """
        Do not return anything, modify head in-place instead.
        """
        if not head or not head.next or not head.next.next:
            return
        
        # Шаг 1: Находим середину списка
        slow, fast = head, head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        
        # Шаг 2: Разделяем список на две половины
        second_half = slow.next
        slow.next = None
        
        # Шаг 3: Реверсируем вторую половину
        prev = None
        curr = second_half
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        second_half = prev
        
        # Шаг 4: Сливаем две половины
        first, second = head, second_half
        while second:
            temp1, temp2 = first.next, second.next
            first.next = second
            second.next = temp1
            first, second = temp1, temp2