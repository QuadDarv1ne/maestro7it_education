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
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    """
    @brief Находит узел, с которого начинается цикл в связном списке
    
    Алгоритм Флойда (черепаха и заяц):
    1. Используем два указателя: медленный (1 шаг) и быстрый (2 шага)
    2. Если указатели встречаются, значит есть цикл
    3. После встречи перемещаем один указатель в начало списка
    4. Двигаем оба указателя по одному шагу, пока они не встретятся
    5. Точка встречи - начало цикла
    
    @param head Начало связного списка
    @return Узел начала цикла или None, если цикла нет
    """
    def detectCycle(self, head):
        if not head or not head.next:
            return None
        
        slow = head
        fast = head
        
        # Шаг 1: Находим точку встречи (если цикл существует)
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                # Шаг 2: Находим начало цикла
                slow = head
                while slow != fast:
                    slow = slow.next
                    fast = fast.next
                return slow  # Начало цикла
        
        return None  # Цикла нет