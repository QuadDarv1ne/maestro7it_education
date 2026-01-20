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
    def minBitwiseArray(self, nums):
        """
        Конструирует минимальный побитовый массив.
        
        Для каждого элемента nums[i] находит минимальное ans[i] такое, что:
        ans[i] OR (ans[i] + 1) == nums[i]
        
        Аргументы:
            nums: список простых чисел
            
        Возвращает:
            список целых чисел, где ans[i] - минимальное значение,
            удовлетворяющее условию, или -1 если невозможно
        """
        ans = []
        
        for x in nums:
            # Если x равно 2, решение невозможно
            if x == 2:
                ans.append(-1)
            else:
                # Находим первый 0-бит справа (после завершающих единиц)
                # Перебираем позиции битов
                for i in range(1, 32):
                    # Проверяем, является ли бит на позиции i нулем
                    if (x >> i) & 1 == 0:
                        # Переворачиваем бит на позиции i-1 для получения минимального ans[i]
                        result = x ^ (1 << (i - 1))
                        ans.append(result)
                        break
        
        return ans


# Альтернативное более чистое решение
class SolutionV2:
    def minBitwiseArray(self, nums):
        """
        Конструирует минимальный побитовый массив (упрощенная версия).
        
        Аргументы:
            nums: список простых чисел
            
        Возвращает:
            список минимальных значений ans[i] или -1
        """
        ans = []
        
        for x in nums:
            if x == 2:
                ans.append(-1)
            else:
                # Находим позицию самого правого 0-бита
                # путем поиска первого 0 после завершающих единиц
                found = False
                for i in range(1, 32):
                    if not (x >> i & 1):  # Проверяем, является ли бит i нулем
                        ans.append(x ^ (1 << (i - 1)))
                        found = True
                        break
        
        return ans