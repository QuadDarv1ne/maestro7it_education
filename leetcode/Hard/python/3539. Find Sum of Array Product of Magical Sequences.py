'''
https://leetcode.com/problems/find-sum-of-array-product-of-magical-sequences/description/?envType=daily-question&envId=2025-10-12
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
'''

class Solution:
    def magicalSum(self, m, k, nums):
        MOD = 10**9 + 7
        n = len(nums)

        # Граничные случаи
        if m == 0:
            return 1 if k == 0 else 0
        if k < 0:
            return 0

        # Предвычислим C[0..m][0..m] (Pascal) для пошагового умножения способов
        C = [[0] * (m + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            C[i][0] = 1
            for j in range(1, i + 1):
                C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD

        # Предвычислим powers: pow_vals[i][t] = nums[i]^t % MOD для t=0..m
        pow_vals = [[1] * (m + 1) for _ in range(n)]
        for i in range(n):
            for t in range(1, m + 1):
                pow_vals[i][t] = (pow_vals[i][t-1] * (nums[i] % MOD)) % MOD

        # DP: текущий по позициям
        # dp[carry][used][pc] = суммарная сумма (prod * ways) для текущих параметров
        # Размеры: carry 0..m, used 0..m, pc 0..k
        # Для экономии памяти будем хранить как список вложенных списков
        dp = [[[0] * (k + 1) for _ in range(m + 1)] for __ in range(m + 1)]
        dp[0][0][0] = 1  # пустая конфигурация: prod=1, ways=1

        for pos in range(n):
            # инициализируем dp_next нулями
            dp_next = [[[0] * (k + 1) for _ in range(m + 1)] for __ in range(m + 1)]
            for carry in range(0, m + 1):
                for used in range(0, m + 1):
                    # если уже использовано больше m — пропускаем
                    if used > m:
                        continue
                    rem = m - used
                    for pc in range(0, k + 1):
                        cur_val = dp[carry][used][pc]
                        if cur_val == 0:
                            continue
                        # пробуем взять take от 0 до rem копий индекса pos
                        # при каждом выборе: множим на nums[pos]^take и на C[rem][take]
                        for take in range(0, rem + 1):
                            prod_mul = pow_vals[pos][take]           # nums[pos]^take % MOD
                            ways_mul = C[rem][take]                 # выбор позиций в последовательности
                            total_mul = cur_val * prod_mul % MOD
                            total_mul = total_mul * ways_mul % MOD

                            total_at_pos = carry + take
                            bit = total_at_pos & 1
                            carry2 = total_at_pos >> 1
                            pc2 = pc + bit
                            if pc2 > k or carry2 > m:
                                continue
                            used2 = used + take
                            dp_next[carry2][used2][pc2] = (dp_next[carry2][used2][pc2] + total_mul) % MOD
            # переходим к следующей позиции
            dp = dp_next

        # После последней позиции: учесть оставшийся carry (он даёт биты старших позиций)
        ans = 0
        for carry in range(0, m + 1):
            # popcount остаточного carry (высшие биты)
            carry_bits = bin(carry).count("1")
            for pc in range(0, k + 1):
                used = m
                val = dp[carry][used][pc]
                if val == 0:
                    continue
                final_pc = pc + carry_bits
                if final_pc == k:
                    ans = (ans + val) % MOD

        return ans

'''
Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
8. Официальный сайт школы Maestro7IT: https://school-maestro7it.ru/
'''