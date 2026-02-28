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
    def concatenatedBinary(self, n):
        """
        Возвращает результат конкатенации двоичных представлений чисел от 1 до n
        по модулю 10^9 + 7.

        Аргументы:
            n (int): Верхняя граница диапазона (1 <= n <= 10^5).

        Возвращает:
            int: Результат вычислений по модулю 1_000_000_007.

        Пример:
            >>> Solution().concatenatedBinary(3)
            27  # так как "1" + "10" + "11" = "11011" = 27 в десятичной
        """
        MOD = 10**9 + 7
        ans = 0
        bits = 0  # количество бит, которое будет занимать следующее число i

        for i in range(1, n + 1):
            # Если i - степень двойки (например, 1, 2, 4, 8...), то количество бит увеличивается
            # Проверка: i & (i - 1) == 0 работает для всех степеней двойки
            if (i & (i - 1)) == 0:
                bits += 1
            # Сдвигаем текущий результат влево на 'bits' бит и добавляем i
            # Операция ans << bits равносильна умножению на 2^bits
            # Обязательно берём модуль на каждом шаге, чтобы избежать переполнения
            ans = ((ans << bits) | i) % MOD

        return ans