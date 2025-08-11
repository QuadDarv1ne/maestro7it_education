'''
https://leetcode.com/problems/snakes-and-ladders/description/?envType=study-plan-v2&envId=top-interview-150
'''

from collections import deque

class Solution:
    def snakesAndLadders(self, board):
        n = len(board)
        board1D = [-1] * (n * n)
        
        idx = 0
        left_to_right = True
        for r in range(n-1, -1, -1):
            row_range = range(n) if left_to_right else range(n-1, -1, -1)
            for c in row_range:
                board1D[idx] = board[r][c]
                idx += 1
            left_to_right = not left_to_right

        visited = [False] * (n * n)
        queue = deque([(0, 0)])  # (index, steps)
        visited[0] = True

        while queue:
            pos, steps = queue.popleft()
            if pos == n * n - 1:
                return steps
            for i in range(1, 7):
                next_pos = pos + i
                if next_pos < n * n:
                    dest = board1D[next_pos]
                    if dest != -1:
                        next_pos = dest - 1
                    if not visited[next_pos]:
                        visited[next_pos] = True
                        queue.append((next_pos, steps + 1))

        return -1

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks