'''
https://leetcode.com/problems/combination-sum/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "1545. Find Kth Bit in Nth Binary String"

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
    def findKthBit(self, n: int, k: int) -> str:
        # Base case: S1 = "0"
        if n == 1:
            return "0"
        
        length = (1 << n) - 1  # 2^n - 1
        mid = (length // 2) + 1
        
        if k == mid:
            return "1"
        elif k < mid:
            # Left half: same as S_{n-1}
            return self.findKthBit(n - 1, k)
        else:
            # Right half: mirrored and inverted
            # Corresponding position in S_{n-1}
            new_k = length - k + 1
            bit = self.findKthBit(n - 1, new_k)
            # Invert the bit
            return "0" if bit == "1" else "1"