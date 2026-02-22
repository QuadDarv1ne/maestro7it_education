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
    def binaryGap(self, n):
        """
        Находит максимальное расстояние между двумя последовательными единицами
        в двоичном представлении числа n.

        Алгоритм:
        Преобразуем число в двоичную строку без префикса '0b'.
        Идём по строке слева направо (от младшего бита к старшему),
        запоминая индекс последней встреченной единицы.
        При каждой новой единице вычисляем расстояние до последней
        и обновляем максимум.

        Аргументы:
            n: Положительное целое число (1 <= n <= 10^9).

        Returns:
            Максимальное расстояние, или 0, если единиц меньше двух.
        """
        binary = bin(n)[2:]
        last_one_index = -1
        max_distance = 0

        for i, bit in enumerate(binary):
            if bit == '1':
                if last_one_index != -1:
                    distance = i - last_one_index
                    if distance > max_distance:
                        max_distance = distance
                last_one_index = i

        return max_distance