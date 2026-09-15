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
    def fairCandySwap(self, aliceSizes, bobSizes):
        """
        Находит размеры коробок для обмена, чтобы у Алисы и Боба стало поровну конфет.

        Алгоритм:
        - Вычисляем общую сумму конфет у Алисы и Боба.
        - Находим разницу diff = (sumA - sumB) // 2.
        - Для каждой коробки Алисы a вычисляем необходимую коробку Боба b = a - diff.
        - Если b есть у Боба (хранится в множестве), возвращаем [a, b].

        Параметры:
        aliceSizes (list[int]) – список коробок Алисы.
        bobSizes   (list[int]) – список коробок Боба.

        Возвращает:
        list[int] – два числа [коробка_Алисы, коробка_Боба].
        """
        sumA = sum(aliceSizes)
        sumB = sum(bobSizes)
        diff = (sumA - sumB) // 2
        setB = set(bobSizes)
        for a in aliceSizes:
            need = a - diff
            if need in setB:
                return [a, need]