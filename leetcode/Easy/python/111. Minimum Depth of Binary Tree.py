'''
https://leetcode.com/problems/minimum-depth-of-binary-tree/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Minimum Depth of Binary Tree"
использует BFS: первый найденный лист даёт ответ.
'''

class Solution(object):
    def minDepth(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        if not root:
            return 0

        from collections import deque
        q = deque([(root, 1)])
        
        while q:
            node, depth = q.popleft()
            
            # Если лист — возвращаем глубину
            if not node.left and not node.right:
                return depth
            
            if node.left:
                q.append((node.left, depth + 1))
            if node.right:
                q.append((node.right, depth + 1))
