'''
https://leetcode.com/problems/fruits-into-baskets-iii/description/?envType=daily-question&envId=2025-08-06
'''

# from typing import List

class Solution:
    # def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
    def numOfUnplacedFruits(self, fruits, baskets):
        """
        Считает, сколько типов фруктов не удалось разместить.

        Почему простой двухуказательный жадный метод даёт WA:
        - Если для большого фрукта пропускаем маленькие корзины слева,
          они остаются доступными для будущих маленьких фруктов.
        - Линейный указатель теряет эти корзины навсегда.

        Правильная идея:
        - Построить сегментное дерево по массиву baskets, храня максимум на отрезке.
        - Для каждого fruit выполнить запрос: найти самый левый индекс i,
          где baskets[i] >= fruit (если такого нет — фрукт «не размещён»).
        - После размещения обновить корзину: baskets[i] = -1 (отметить как занятую).

        Сложность:
        - Время: O(n log n), n — число фруктов/корзин.
        - Память: O(n) на дерево.
        """
        n = len(baskets)
        if n == 0:
            return 0

        size = 1
        while size < n:
            size <<= 1
        # Сегдерево на максимумы
        seg = [ -1 ] * (2 * size)

        # build
        for i in range(n):
            seg[size + i] = baskets[i]
        for i in range(size - 1, 0, -1):
            seg[i] = max(seg[i << 1], seg[i << 1 | 1])

        def query_first_ge(x):
            """Возвращает самый левый индекс с значением >= x, либо -1, если не найден."""
            idx = 1
            if seg[idx] < x:
                return -1
            l, r = 0, size - 1
            while l != r:
                mid = (l + r) // 2
                left = idx << 1
                if seg[left] >= x:
                    idx = left
                    r = mid
                else:
                    idx = left | 1
                    l = mid + 1
            # l может выходить за исходный n (пустые хвосты = -1)
            return l if l < n else -1

        def update(pos, val):
            """a[pos] = val"""
            i = pos + size
            seg[i] = val
            i >>= 1
            while i:
                seg[i] = max(seg[i << 1], seg[i << 1 | 1])
                i >>= 1

        unplaced = 0
        for f in fruits:
            i = query_first_ge(f)
            if i == -1:
                unplaced += 1
            else:
                update(i, -1)  # заняли корзину
        return unplaced

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks