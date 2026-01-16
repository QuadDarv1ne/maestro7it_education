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

"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head):
        """
        Создает глубокую копию связанного списка с random указателями.
        
        Алгоритм (HashMap):
        1. Создаем словарь для отображения оригинальных узлов на копии
        2. Первый проход: создаем все копии узлов
        3. Второй проход: устанавливаем next и random связи
        
        Сложность: O(n) время, O(n) память
        """
        
        if not head:
            return None
        
        # Словарь для отображения оригинальных узлов на копии
        node_map = {}
        
        # Первый проход: создаем копии всех узлов
        current = head
        while current:
            node_map[current] = Node(current.val)
            current = current.next
        
        # Второй проход: устанавливаем связи
        current = head
        while current:
            # Устанавливаем next связь
            if current.next:
                node_map[current].next = node_map[current.next]
            
            # Устанавливаем random связь
            if current.random:
                node_map[current].random = node_map[current.random]
            
            current = current.next
        
        return node_map[head]