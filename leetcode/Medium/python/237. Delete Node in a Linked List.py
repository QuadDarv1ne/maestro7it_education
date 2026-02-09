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
    def deleteNode(self, node):
        """
        Удаляет узел из односвязного списка без доступа к голове списка.
        
        Алгоритм:
        1. Копирует значение следующего узла в текущий узел.
        2. Изменяет указатель текущего узла на узел через один (пропускает следующий узел).
        
        Сложность:
        Время: O(1)
        Пространство: O(1)
        
        Параметры:
        ----------
        node : ListNode
            Узел, который нужно удалить из списка
            
        Возвращает:
        -----------
        None
            Функция модифицирует список на месте
            
        Пример:
        -------
        Исходный список: 4 -> 5 -> 1 -> 9
        Удаляем узел со значением 5
        Результат: 4 -> 1 -> 9
        
        Примечание:
        -----------
        - Узел не является хвостовым (гарантируется, что node.next != None)
        - Не нужно освобождать память в Python
        """
        # Копируем значение следующего узла в текущий узел
        node.val = node.next.val
        
        # Пропускаем следующий узел
        node.next = node.next.next
    
    def deleteNode_alternative(self, node):
        """
        Альтернативная реализация с явным сохранением следующего узла.
        
        Параметры:
        ----------
        node : ListNode
            Узел для удаления
        """
        # Получаем следующий узел
        next_node = node.next
        
        # Копируем значение и указатель следующего узла
        node.val = next_node.val
        node.next = next_node.next
        
        # В Python не нужно явно удалять next_node, сборщик мусора сделает это