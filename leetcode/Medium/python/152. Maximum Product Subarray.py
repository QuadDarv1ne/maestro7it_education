'''
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. YouTube канал: https://www.youtube.com/@it-coders
6. ВК группа: https://vk.com/science_geeks
'''

class Solution:
    def maxProduct(self, nums):
        """
        Находит максимальное произведение подмассива.
        
        Параметры:
        nums - список целых чисел
        
        Возвращает:
        Максимальное произведение подмассива
        
        Алгоритм:
        - Используем динамическое программирование с двумя переменными:
          max_prod - максимальное произведение до текущего элемента
          min_prod - минимальное произведение до текущего элемента
        - При встрече отрицательного числа меняем max и min местами
        - На каждом шаге обновляем результат
        """
        if not nums:
            return 0
        
        # Инициализируем переменные первым элементом
        max_prod = min_prod = result = nums[0]
        
        for i in range(1, len(nums)):
            current = nums[i]
            
            # Если текущее число отрицательное, меняем местами max и min
            # (потому что при умножении на отрицательное число знаки меняются)
            if current < 0:
                max_prod, min_prod = min_prod, max_prod
            
            # Обновляем максимальное и минимальное произведение
            max_prod = max(current, max_prod * current)
            min_prod = min(current, min_prod * current)
            
            # Обновляем общий результат
            result = max(result, max_prod)
        
        return result