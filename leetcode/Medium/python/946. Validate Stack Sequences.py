'''
https://leetcode.com/problems/validate-stack-sequences/description/
'''

class Solution:
    def validateStackSequences(self, pushed, popped):
        """
        Проверяет, можно ли из последовательности pushed
        получить последовательность popped с помощью операций стека.
        
        :param pushed: список чисел, которые кладутся в стек
        :param popped: список чисел, которые должны быть извлечены
        :return: True, если popped достижим, иначе False

        Алгоритм:
        1. Добавляем элементы из pushed в стек.
        2. Если верхушка совпадает с текущим элементом popped,
           извлекаем и двигаем указатель по popped.
        3. В конце проверяем, все ли элементы popped были извлечены.

        Временная сложность: O(n) — каждый элемент кладётся и извлекается максимум 1 раз.
        Память: O(n) для стека.
        """
        stack, j = [], 0
        for x in pushed:
            stack.append(x)
            while stack and stack[-1] == popped[j]:
                stack.pop()
                j += 1
        return j == len(popped)

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks