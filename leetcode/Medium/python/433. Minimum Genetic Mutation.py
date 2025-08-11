'''
https://leetcode.com/problems/minimum-genetic-mutation/description/?envType=study-plan-v2&envId=top-interview-150
'''

from collections import deque

class Solution:
    def minMutation(self, startGene, endGene, bank):
        bank = set(bank)
        if endGene not in bank:
            return -1

        queue = deque([(startGene, 0)])

        while queue:
            current_gene, level = queue.popleft()

            for i in range(len(current_gene)):
                for char in 'ACGT':
                    next_gene = current_gene[:i] + char + current_gene[i+1:]
                    if next_gene == endGene:
                        return level + 1
                    if next_gene in bank:
                        bank.remove(next_gene)
                        queue.append((next_gene, level + 1))

        return -1

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks