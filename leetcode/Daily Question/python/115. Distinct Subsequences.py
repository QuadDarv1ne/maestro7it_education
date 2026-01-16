"""
Подсчёт количества вхождений строки t как подпоследовательности в строку s

@param s: Исходная строка, в которой ищем подпоследовательности
@param t: Строка, которую ищем как подпоследовательность
@return: Количество различных способов получить t как подпоследовательность s

Сложность: Время O(m×n), Память O(n), где m = len(s), n = len(t)

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
    def numDistinct(self, s, t):
        m, n = len(s), len(t)
        
        # Базовые случаи
        if m < n:
            return 0
        if n == 0:
            return 1
        
        # Используем список для динамического программирования
        dp = [0] * (n + 1)
        dp[0] = 1  # Пустая подпоследовательность
        
        # Проходим по строке s
        for i in range(m):
            # Проходим по строке t справа налево
            for j in range(n - 1, -1, -1):
                if s[i] == t[j]:
                    dp[j + 1] += dp[j]
        
        return dp[n]