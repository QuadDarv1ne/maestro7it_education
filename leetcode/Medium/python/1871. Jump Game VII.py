"""
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
"""

class Solution:
    def canReach(self, s, minJump, maxJump):
        """
        Решение задачи Jump Game VII.
        
        Определяет, можно ли добраться до последнего индекса бинарной строки s,
        начиная с индекса 0.

        Алгоритм использует скользящее окно для отслеживания количества достижимых
        позиций в диапазоне [i - maxJump, i - minJump], из которых можно попасть в i.
        Это позволяет решить задачу за линейное время O(N).

        Args:
            s: Бинарная строка, содержащая только символы '0' и '1'.
            minJump: Минимальная длина прыжка.
            maxJump: Максимальная длина прыжка.

        Returns:
            True, если последний индекс достижим, иначе False.
        """
        n = len(s)
        dp = [False] * n
        dp[0] = True
        count = 0
        
        for i in range(1, n):
            if i >= minJump:
                if dp[i - minJump]:
                    count += 1
            
            if i > maxJump:
                if dp[i - maxJump - 1]:
                    count -= 1
            
            if s[i] == '0' and count > 0:
                dp[i] = True
                
        return dp[n - 1]