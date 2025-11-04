'''
https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
'''

class Solution(object):
    def strStr(self, haystack, needle):
        """
        Решение задачи "Find the Index of the First Occurrence in a String" (LeetCode 28).

        Идея:
        - Используем встроенный метод find() строки, который возвращает
          индекс первого вхождения подстроки или -1, если не найдено.
        - Альтернатива — реализация через цикл и срезы (O(n·m)), но стандартная
          реализация Python (Boyer-Moore или KMP в оптимизированных версиях C)
          обычно достаточно эффективна для большинства случаев.

        Сложность:
        - Время: O(n·m) в худшем случае (гарантированно)
        - Память: O(1)
        """
        return haystack.find(needle)
    
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks