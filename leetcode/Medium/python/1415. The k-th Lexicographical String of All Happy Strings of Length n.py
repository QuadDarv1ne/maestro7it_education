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
    def getHappyString(self, n: int, k: int) -> str:
        # Общее количество счастливых строк = 3 * 2^(n-1)
        total = 3 * (1 << (n - 1))  # 1 << (n-1) это 2^(n-1)
        if k > total:
            return ""

        result = []
        prev = ''  # предыдущий символ (пусто для первого символа)

        for i in range(n):
            # Перебираем символы в лексикографическом порядке
            for c in ('a', 'b', 'c'):
                # Пропускаем символ, равный предыдущему
                if c == prev:
                    continue

                # Количество строк с текущим префиксом для оставшихся позиций
                # Для каждой оставшейся позиции есть 2 варианта (кроме предыдущего)
                count = 1 << (n - i - 1)  # 2^(n - i - 1)

                if k > count:
                    # Искомая строка находится в следующем блоке
                    k -= count
                else:
                    # Нашли нужный символ
                    result.append(c)
                    prev = c
                    break

        return ''.join(result)