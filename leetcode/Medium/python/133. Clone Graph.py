'''
https://leetcode.com/problems/clone-graph/description/
'''

# from typing import List, Optional

# class Node:
#     def __init__(self, val: int = 0, neighbors: Optional[List['Node']] = None):
#         self.val = val
#         self.neighbors = neighbors if neighbors is not None else []

class Solution:
    # def cloneGraph(self, node: 'Node') -> 'Node':
    def cloneGraph(self, node):
        """
        Клонирует связный неориентированный граф.
        Используется DFS с словарем для отслеживания уже клонированных узлов.

        :param node: узел графа
        :return: глубокая копия графа
        """
        if not node:
            return None
        
        visited = {}
        
        # def dfs(n: 'Node') -> 'Node':
        def dfs(n):
            if n.val in visited:
                return visited[n.val]
            
            clone_node = Node(n.val)
            visited[n.val] = clone_node
            
            for neighbor in n.neighbors:
                clone_node.neighbors.append(dfs(neighbor))
            
            return clone_node
        
        return dfs(node)

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks