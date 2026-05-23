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
    def check(self, nums):
        """
        Проверяет, может ли массив nums быть получен из отсортированного
        по неубыванию массива путём вращения (сдвига) на несколько позиций.

        Алгоритм:
        Свойство такого массива — наличие не более одного "перепада"
        (nums[i] > nums[i+1]). Дополнительно проверяется, что последний
        элемент не больше первого, чтобы гарантировать корректную "склейку"
        оригинального отсортированного массива.

        Сложность:
            - Время: O(n)
            - Память: O(1)

        Аргументы:
            nums (List[int]): Входной массив целых чисел.

        Возвращает:
            bool: True, если массив можно получить вращением отсортированного,
                  иначе False.
        """
        n = len(nums)
        count_breaks = 0  # Счётчик "перепадов"

        # Считаем количество мест, где текущий элемент больше следующего
        for i in range(n - 1):
            if nums[i] > nums[i + 1]:
                count_breaks += 1

        # Если перепадов больше одного, это не может быть повёрнутым отсортированным массивом
        if count_breaks > 1:
            return False
        
        # Если перепад ровно один, проверяем условие "склейки" концов
        if count_breaks == 1:
            return nums[-1] <= nums[0]

        # Если перепадов 0, массив уже отсортирован
        return True