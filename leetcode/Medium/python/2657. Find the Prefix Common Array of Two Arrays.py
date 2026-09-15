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
    def findThePrefixCommonArray(self, A, B):
        """
        Возвращает префиксный массив общих элементов C для двух перестановок A и B.

        C[i] равно количеству чисел, которые присутствуют в A[0..i] и B[0..i]
        одновременно. Так как A и B — перестановки чисел от 1 до n, каждое число
        встречается ровно один раз в каждом массиве.

        Алгоритм:
        Используем массив счётчиков count для чисел от 1 до n. На каждом шаге i
        увеличиваем счётчики для A[i] и B[i]. Если какое-то число уже встречалось
        ранее (счётчик стал 2), значит оно появилось в обоих массивах на позициях
        не больше i — увеличиваем текущий счётчик общих чисел.
        Результат записываем в C[i].

        Сложность: O(n) по времени, O(n) по памяти.

        Аргументы:
            A: Первая перестановка чисел от 1 до n.
            B: Вторая перестановка чисел от 1 до n.

        Возвращает:
            Список C длиной n, где C[i] — количество общих чисел на префиксе i.
        """
        n = len(A)
        count = [0] * (n + 1)
        result = []
        common = 0

        for i in range(n):
            count[A[i]] += 1
            if count[A[i]] == 2:
                common += 1

            count[B[i]] += 1
            if count[B[i]] == 2:
                common += 1

            result.append(common)

        return result