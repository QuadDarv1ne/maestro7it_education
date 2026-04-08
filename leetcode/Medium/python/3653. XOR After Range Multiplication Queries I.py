"""
https://leetcode.com/problems/xor-after-range-multiplication-queries-i/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "XOR After Range Multiplication Queries I" на Python

Задача: Дан массив nums и список запросов.
Каждый запрос [l, r, k, v] означает: для всех индексов i от l до r с шагом k: nums[i] = (nums[i] * v) % MOD.
После всех запросов нужно вернуть XOR всех элементов массива.

Алгоритм (прямой):
1. Проходим по каждому запросу.
2. Для каждого запроса проходим по индексам i = l; i <= r; i += k.
3. Обновляем nums[i] = (nums[i] * v) % MOD.
4. После всех запросов вычисляем XOR всех элементов.

Сложность: O(q * n) времени, O(1) дополнительной памяти.

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. YouTube канал: https://www.youtube.com/@it-coders
6. ВК группа: https://vk.com/science_geeks

"""

class Solution:
    def xorAfterQueries(self, nums, queries):
        MOD = 10**9 + 7
        
        for l, r, k, v in queries:
            for i in range(l, r + 1, k):
                nums[i] = (nums[i] * v) % MOD
        
        result = 0
        for num in nums:
            result ^= num
        return result