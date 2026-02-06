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

# Python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BSTIterator:
    """
    Итератор для inorder обхода бинарного дерева поиска.
    Использует стек для контролируемого обхода без рекурсии.
    
    Подход:
    1. Конструктор: добавляем в стек все левые узлы от корня
    2. next(): извлекаем вершину стека, если есть правый потомок - 
       добавляем его левую ветку в стек
    3. hasNext(): проверяем, не пуст ли стек
    
    Сложность по времени: O(1) amortized для next(), O(1) для hasNext()
    Сложность по памяти: O(h), где h - высота дерева
    """
    
    def __init__(self, root):
        self.stack = []
        self._push_all_left(root)
    
    def _push_all_left(self, node):
        """Добавляет в стек все узлы левой ветки"""
        while node:
            self.stack.append(node)
            node = node.left
    
    def next(self):
        """Возвращает следующий наименьший элемент"""
        node = self.stack.pop()
        
        if node.right:
            self._push_all_left(node.right)
        
        return node.val
    
    def hasNext(self):
        """Проверяет, есть ли следующий элемент"""
        return len(self.stack) > 0