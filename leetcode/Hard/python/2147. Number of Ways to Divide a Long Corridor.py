'''
https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def numberOfWays(self, corridor):
        MOD = 10**9 + 7

        # Индексы всех сидений
        seats = []
        for i, ch in enumerate(corridor):
            if ch == 'S':
                seats.append(i)

        # Сидений должно быть чётное количество
        if len(seats) < 2 or len(seats) % 2 != 0:
            return 0

        ways = 1

        # Идём по парам сегментов
        for i in range(1, len(seats) - 1, 2):
            # расстояние между сегментами
            gap = seats[i + 1] - seats[i]
            ways = (ways * gap) % MOD

        return ways
