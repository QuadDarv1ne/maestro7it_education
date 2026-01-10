"""
Минимальная сумма ASCII-кодов удаленных символов для двух строк

@param s1 Первая строка
@param s2 Вторая строка
@return Минимальная сумма ASCII-кодов удаленных символов

Сложность: Время O(m*n), Память O(m*n), где m и n - длины строк

Автор: Дуплей Максим Игоревич
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
    def minimumDeleteSum(self, s1, s2):
        m, n = len(s1), len(s2)
        
        # dp[i][j] - минимальная стоимость для s1[0:i] и s2[0:j]
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Инициализация: удаление всех символов из s1
        for i in range(1, m + 1):
            dp[i][0] = dp[i - 1][0] + ord(s1[i - 1])
        
        # Инициализация: удаление всех символов из s2
        for j in range(1, n + 1):
            dp[0][j] = dp[0][j - 1] + ord(s2[j - 1])
        
        # Заполнение таблицы DP
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    # Символы совпадают - не нужно удалять
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # Выбираем минимум из двух вариантов:
                    # 1. Удалить символ из s1
                    # 2. Удалить символ из s2
                    dp[i][j] = min(
                        dp[i - 1][j] + ord(s1[i - 1]),
                        dp[i][j - 1] + ord(s2[j - 1])
                    )
        
        return dp[m][n]