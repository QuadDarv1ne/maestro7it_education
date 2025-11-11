'''
https://leetcode.com/problems/swap-nodes-in-pairs/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
'''

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution(object):
    def swapPairs(self, head):
        """
        Решение задачи "Swap Nodes in Pairs" (LeetCode 24).

        Идея:
        - Используем фиктивный узел (dummy), чтобы упростить обработку головы списка.
        - Указатель prev ссылается на узел перед текущей парой.
        - Пока есть как минимум два узла (head и head.next):
            • Меняем местами first и second.
            • Обновляем связи: prev → second → first → (оставшийся список).
            • Сдвигаем prev на first, а head — на следующий узел после first.
        - Возвращаем dummy.next как новую голову списка.
        
        Сложность:
        - Время: O(n)
        - Память: O(1)
        """
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy
        
        while head and head.next:
            first = head
            second = head.next
            
            # Перестановка
            prev.next = second
            first.next = second.next
            second.next = first
            
            # Подготовка к следующей итерации
            prev = first
            head = first.next
        
        return dummy.next

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07  
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/  
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ  
# 6. YouTube канал: https://www.youtube.com/@it-coders  
# 7. ВК группа: https://vk.com/science_geeks