'''
https://leetcode.com/problems/combination-sum-ii/description/
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
'''

class Solution:
    def numberOfStableArrays(self, zero, one, limit):
        MOD = 10**9 + 7
        # dp0[z][o] – массивы, заканчивающиеся на 0
        # dp1[z][o] – заканчивающиеся на 1
        dp0 = [[0] * (one + 1) for _ in range(zero + 1)]
        dp1 = [[0] * (one + 1) for _ in range(zero + 1)]

        # База: только нули или только единицы
        for z in range(1, min(zero, limit) + 1):
            dp0[z][0] = 1
        for o in range(1, min(one, limit) + 1):
            dp1[0][o] = 1

        # sum1[z] – скользящая сумма последних limit значений dp0[z][*] по o
        sum1 = [0] * (zero + 1)

        for o in range(one + 1):
            # 1. Обновляем sum1 для текущего o
            if o > 0:
                for z in range(zero + 1):
                    sum1[z] = (sum1[z] + dp0[z][o - 1]) % MOD
                    if o - limit - 1 >= 0:
                        sum1[z] = (sum1[z] - dp0[z][o - limit - 1]) % MOD

            # 2. Вычисляем dp1[z][o]
            if o > 0:
                for z in range(zero + 1):
                    val = sum1[z]
                    if z == 0 and o <= limit:          # последовательность из одних единиц
                        val = (val + 1) % MOD
                    dp1[z][o] = val

            # 3. Вычисляем dp0[z][o] скользящей суммой по z
            cur_sum = 0
            for z in range(zero + 1):
                if z > 0:
                    cur_sum = (cur_sum + dp1[z - 1][o]) % MOD
                    if z - limit - 1 >= 0:
                        cur_sum = (cur_sum - dp1[z - limit - 1][o]) % MOD
                if o > 0:
                    dp0[z][o] = cur_sum
                # для o = 0 значения уже заданы в базе

        return (dp0[zero][one] + dp1[zero][one]) % MOD
