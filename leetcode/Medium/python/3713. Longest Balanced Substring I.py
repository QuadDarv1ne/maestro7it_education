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
    def longestBalanced(self, s):
        """
        Возвращает длину самой длинной сбалансированной подстроки.

        Сбалансированная подстрока — это подстрока, в которой все различные
        символы встречаются одинаковое количество раз.

        Алгоритм:
            Полный перебор всех подстрок. Для каждой начальной позиции i
            последовательно расширяем правую границу j, обновляя счётчик
            частот символов. Проверяем, равны ли частоты всех различных
            символов в текущей подстроке. Если да — обновляем максимум.

        Сложность:
            Время: O(26 * n^2) ≈ O(n^2) при n ≤ 1000.
            Память: O(1) — массив фиксированного размера 26.

        Аргументы:
            s (str): Исходная строка из строчных латинских букв.

        Возвращает:
            int: Максимальная длина сбалансированной подстроки.
        """
        n = len(s)
        max_len = 0

        for i in range(n):
            freq = [0] * 26          # частоты символов для подстрок, начинающихся с i
            for j in range(i, n):
                # добавляем текущий символ
                freq[ord(s[j]) - ord('a')] += 1

                min_freq = float('inf')
                max_freq = 0
                for cnt in freq:
                    if cnt > 0:
                        if cnt < min_freq:
                            min_freq = cnt
                        if cnt > max_freq:
                            max_freq = cnt

                # если все ненулевые частоты равны, подстрока сбалансирована
                if min_freq == max_freq:
                    max_len = max(max_len, j - i + 1)

        return max_len