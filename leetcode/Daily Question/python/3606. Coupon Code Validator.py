'''
https://leetcode.com/problems/coupon-code-validator/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

import re

class Solution:
    def validateCoupons(self, code, businessLine, isActive):
        """
        Решение задачи "Coupon Code Validator" (LeetCode 3606).

        Идея:
        - Проверяем каждый купон на валидность:
          - code не пустой и содержит только допустимые символы,
          - businessLine входит в фиксированный список,
          - isActive == True.
        - Сортируем по order бизнес‑линий и по коду.

        Сложность:
        - Время: O(n log n)
        - Память: O(n)
        """
        valid_lines_order = ["electronics", "grocery", "pharmacy", "restaurant"]
        valid_set = set(valid_lines_order)

        valid_coupons = []
        pattern = re.compile(r"^[A-Za-z0-9_]+$")

        for c, bl, active in zip(code, businessLine, isActive):
            if active and bl in valid_set and c and pattern.match(c):
                valid_coupons.append((bl, c))

        # Сортируем сначала по category order, потом по code лексикографически
        valid_coupons.sort(key=lambda x: (valid_lines_order.index(x[0]), x[1]))

        return [code for _, code in valid_coupons]
