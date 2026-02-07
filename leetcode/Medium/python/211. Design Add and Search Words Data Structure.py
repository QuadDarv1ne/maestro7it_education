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

# class TrieNode:
#     """Узел префиксного дерева"""
#     def __init__(self):
#         self.children = {}  # Словарь для хранения детей
#         self.is_end = False  # Флаг конца слова

class WordDictionary:
    """
    Структура данных для добавления и поиска слов с поддержкой wildcard '.'
    
    Особенности:
    - addWord(word): добавляет слово в структуру
    - search(word): ищет слово, '.' соответствует любому символу
    
    Сложности:
    - Добавление: O(n), где n - длина слова
    - Поиск: в худшем случае O(26^n) при всех '.', но обычно гораздо меньше
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word: str) -> None:
        """Добавляет слово в структуру"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        """Ищет слово, '.' соответствует любому символу"""
        def dfs(node, index):
            # Базовый случай: дошли до конца слова
            if index == len(word):
                return node.is_end
            
            char = word[index]
            
            # Если символ - точка, проверяем всех детей
            if char == '.':
                for child in node.children.values():
                    if dfs(child, index + 1):
                        return True
                return False
            # Если символ обычный
            else:
                if char not in node.children:
                    return False
                return dfs(node.children[char], index + 1)
        
        return dfs(self.root, 0)