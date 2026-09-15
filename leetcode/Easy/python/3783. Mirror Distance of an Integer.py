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
    def mirrorDistance(self, n):
        """
        Вычисляет зеркальное расстояние числа n.

        Зеркальное расстояние определяется как |n - reverse(n)|,
        где reverse(n) - число, полученное записью цифр n в обратном порядке.

        Args:
            n: Исходное целое число.

        Returns:
            Целое число, представляющее зеркальное расстояние.
        """
        # 1. Преобразуем число в строку, переворачиваем её и преобразуем обратно в число.
        #    Это автоматически отбросит ведущие нули (например, reverse(10) станет 1).
        reversed_n = int(str(n)[::-1])
        
        # 2. Возвращаем абсолютную разницу.
        return abs(n - reversed_n)