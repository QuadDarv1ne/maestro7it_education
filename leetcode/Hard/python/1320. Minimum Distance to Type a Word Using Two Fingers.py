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

# Python
class Solution:
    """
    LeetCode 1320. Minimum Distance to Type a Word Using Two Fingers  [Python]

    Условие:
        Клавиатура — сетка 6×4 (A='(0,0)', B='(0,1)', ..., Z='(5,1)').
        Расстояние между клавишами = манхэттенское расстояние.
        Напечатать слово двумя пальцами; оба пальца стартуют бесплатно
        с произвольных позиций. Найти минимальную суммарную стоимость.

    Подход — Динамическое программирование (DP):
        Состояние dp[i][j]:
            • первый палец только что нажал word[i]
            • второй палец стоит на позиции j  (26 = не размещён)

        Переходы при печати word[i+1]:
            1) Двигаем первый палец → word[i+1]:
               dp[i+1][j]   = min(dp[i+1][j],   dp[i][j] + dist(cur, nxt))
            2) Двигаем второй палец → word[i+1],
               первый "замирает" на cur:
               dp[i+1][cur] = min(dp[i+1][cur], dp[i][j] + dist(j, nxt))
               Если j == 26 — стоимость перемещения = 0.

        Ответ: min(dp[n-1]).

    Сложность:
        Время:  O(n × 27)
        Память: O(n × 27)
    """

    def minimumDistance(self, word):
        """
        Находит минимальное суммарное расстояние для набора слова двумя пальцами.

        :param word: строка из заглавных латинских букв
        :return:     минимальная суммарная стоимость перемещений
        """

        def dist(a, b):
            """Манхэттенское расстояние между буквами a и b (0-индекс A-Z)."""
            return abs(a // 6 - b // 6) + abs(a % 6 - b % 6)

        INF = float('inf')
        n = len(word)

        dp = [[INF] * 27 for _ in range(n)]
        dp[0][26] = 0  # первый палец бесплатно на word[0], второй не размещён

        for i in range(n - 1):
            cur = ord(word[i])     - ord('A')
            nxt = ord(word[i + 1]) - ord('A')

            for j in range(27):
                if dp[i][j] == INF:
                    continue
                cost_j = 0 if j == 26 else dist(j, nxt)

                # Вариант 1: первый палец → nxt, второй остаётся на j
                dp[i+1][j]   = min(dp[i+1][j],   dp[i][j] + dist(cur, nxt))
                # Вариант 2: второй палец → nxt, первый замирает на cur
                dp[i+1][cur] = min(dp[i+1][cur], dp[i][j] + cost_j)

        return min(dp[n-1])