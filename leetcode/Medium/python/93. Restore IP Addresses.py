'''
https://leetcode.com/problems/restore-ip-addresses/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution(object):
    def restoreIpAddresses(self, s):
        """
        Решение задачи "Restore IP Addresses" (LeetCode 93).

        Задача:
        - Дан строковый набор цифр s.
        - Вернуть все возможные допустимые IP‑адреса, разбив
          s на 4 части (0−255), без ведущих нулей
          (кроме «0» как отдельной части).

        Идея:
        - Используем backtracking: выбираем 4 части,
          длина каждой от 1 до 3.
        - Проверяем, что каждая часть в допустимом диапазоне
          и не содержит ведущих нулей.
        - Если удалось выбрать ровно 4 части и строка
          полностью использована — сохраняем.

        Сложность:
        - Время: O(3⁴·n) ≈ O(n)
        - Память: O(1)
        """
        res = []

        def backtrack(start, parts):
            if len(parts) == 4:
                if start == len(s):
                    res.append(".".join(parts))
                return

            # Обрезаем слишком длинные остатки
            if start >= len(s):
                return

            # Генерируем следующие части (1 до 3 символов)
            for length in range(1, 4):
                if start + length > len(s):
                    break
                segment = s[start:start+length]
                # Проверка ведущих нулей
                if segment.startswith("0") and length > 1:
                    continue
                # Проверка диапазона 0‑255
                if int(segment) <= 255:
                    parts.append(segment)
                    backtrack(start+length, parts)
                    parts.pop()

        backtrack(0, [])
        return res
