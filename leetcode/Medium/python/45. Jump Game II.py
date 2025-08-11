'''
https://leetcode.com/problems/jump-game-ii/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution:
    def jump(self, nums):
        """
        Определяет минимальное количество прыжков, необходимых для достижения
        конца массива, где каждый элемент массива nums[i] — максимальная длина
        прыжка с позиции i.

        Параметры:
        -----------
        nums : List[int]
            Список целых чисел, где nums[i] — максимально возможный шаг из позиции i.

        Возвращаемое значение:
        ----------------------
        int
            Минимальное число прыжков, чтобы добраться до последнего индекса массива.

        Описание решения:
        -----------------
        Используется жадный алгоритм:
        - Проходим по массиву, отслеживая максимальную дальность прыжка (farthest),
          которую можно достигнуть с текущего количества прыжков.
        - current_end — граница текущего диапазона прыжков; когда достигаем её,
          увеличиваем счётчик прыжков и обновляем границу на farthest.
        - Таким образом минимизируем количество прыжков.

        Сложность:
        ----------
        Временная: O(n), где n — длина массива nums.
        По памяти: O(1).

        Пример:
        --------
        nums = [2, 3, 1, 1, 4]
        Результат: 2
        Пояснение: прыжок с позиции 0 на 1, затем с позиции 1 на 4 (конец массива).
        """
        jumps = 0
        current_end = 0
        farthest = 0
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == current_end:
                jumps += 1
                current_end = farthest
        return jumps

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks