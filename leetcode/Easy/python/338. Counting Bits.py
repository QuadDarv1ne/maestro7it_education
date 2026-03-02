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
    def countBits(self, n):
        """
        Возвращает массив количества единичных битов для всех чисел от 0 до n.
        
        Используется динамическое программирование:
        - Для чётного i: ans[i] = ans[i // 2]
        - Для нечётного i: ans[i] = ans[i - 1] + 1
        Объединённая формула: ans[i] = ans[i >> 1] + (i & 1)
        """
        ans = [0] * (n + 1)
        for i in range(1, n + 1):
            # i >> 1 — это i // 2, (i & 1) даёт 1 для нечётных i и 0 для чётных
            ans[i] = ans[i >> 1] + (i & 1)
        return ans