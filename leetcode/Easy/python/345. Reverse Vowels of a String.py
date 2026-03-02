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
    def reverseVowels(self, s):
        """
        Переворачивает только гласные буквы в строке.
        
        Алгоритм:
        1. Создаём множество гласных (включая заглавные).
        2. Преобразуем строку в список для изменения.
        3. Используем два указателя с обоих концов.
        4. Меняем местами найденные гласные.
        
        Аргументы:
            s (str): исходная строка.
        
        Возвращает:
            str: строка с перевёрнутыми гласными.
        """
        vowels = set('aeiouAEIOU')
        s_list = list(s)
        left, right = 0, len(s) - 1
        
        while left < right:
            # Двигаем левый указатель до гласной
            while left < right and s_list[left] not in vowels:
                left += 1
            # Двигаем правый указатель до гласной
            while left < right and s_list[right] not in vowels:
                right -= 1
            # Меняем местами
            if left < right:
                s_list[left], s_list[right] = s_list[right], s_list[left]
                left += 1
                right -= 1
                
        return ''.join(s_list)