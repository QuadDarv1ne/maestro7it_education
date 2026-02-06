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

# Python
class Solution:
    """
    Находит два числа в отсортированном массиве, сумма которых равна target.
    Возвращает 1-индексированные позиции этих чисел.
    
    Подход:
    1. Используем два указателя: left в начале, right в конце
    2. Вычисляем сумму numbers[left] + numbers[right]
    3. Если sum == target → возвращаем индексы
    4. Если sum < target → сдвигаем left вправо (увеличиваем сумму)
    5. Если sum > target → сдвигаем right влево (уменьшаем сумму)
    
    Сложность по времени: O(n)
    Сложность по памяти: O(1)
    """
    
    def twoSum(self, numbers, target):
        left = 0
        right = len(numbers) - 1
        
        while left < right:
            current_sum = numbers[left] + numbers[right]
            
            if current_sum == target:
                # Возвращаем 1-индексированные позиции
                return [left + 1, right + 1]
            elif current_sum < target:
                # Нужна большая сумма - сдвигаем left вправо
                left += 1
            else:
                # Нужна меньшая сумма - сдвигаем right влево
                right -= 1
        
        return [-1, -1]