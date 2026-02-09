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
    def isPalindrome(self, head):
        """
        Проверяет, является ли односвязный список палиндромом.
        
        Алгоритм:
        1. Находит середину списка с помощью быстрого и медленного указателей.
        2. Разворачивает вторую половину списка.
        3. Сравнивает первую и развернутую вторую половины.
        4. (Опционально) Восстанавливает исходный список.
        
        Сложность:
        Время: O(n), где n - количество узлов в списке
        Пространство: O(1), используем только указатели
        
        Параметры:
        ----------
        head : ListNode
            Голова односвязного списка
            
        Возвращает:
        -----------
        bool
            True, если список является палиндромом, иначе False
            
        Примеры:
        --------
        Вход: 1->2->2->1
        Выход: True
        
        Вход: 1->2
        Выход: False
        """
        if not head or not head.next:
            return True
        
        # Шаг 1: Находим середину списка
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Шаг 2: Разворачиваем вторую половину
        second_half = self._reverse_list(slow)
        
        # Шаг 3: Сравниваем две половины
        first_half = head
        second_half_copy = second_half
        result = True
        
        while second_half:
            if first_half.val != second_half.val:
                result = False
                break
            first_half = first_half.next
            second_half = second_half.next
        
        # Шаг 4: Восстанавливаем исходный список (опционально)
        self._reverse_list(second_half_copy)
        
        return result
    
    def _reverse_list(self, head):
        """
        Разворачивает односвязный список.
        
        Параметры:
        ----------
        head : ListNode
            Голова списка для разворота
            
        Возвращает:
        -----------
        ListNode
            Голова развернутого списка
        """
        prev = None
        current = head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        return prev
    
    def isPalindrome_with_array(self, head):
        """
        Альтернативное решение с использованием массива.
        Проще, но использует O(n) дополнительной памяти.
        
        Параметры:
        ----------
        head : ListNode
            Голова списка
            
        Возвращает:
        -----------
        bool
            True, если список является палиндромом
        """
        values = []
        current = head
        
        # Собираем значения в массив
        while current:
            values.append(current.val)
            current = current.next
        
        # Проверяем, является ли массив палиндромом
        left, right = 0, len(values) - 1
        while left < right:
            if values[left] != values[right]:
                return False
            left += 1
            right -= 1
        
        return True