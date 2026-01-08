'''
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
'''

# from typing import List

class Solution:
    """
    Максимальное скалярное произведение двух подпоследовательностей
    
    Args:
        nums1 (List[int]): Первый массив целых чисел
        nums2 (List[int]): Второй массив целых чисел
    
    Returns:
        int: Максимальное скалярное произведение
        
    Сложность: Время O(m*n), Память O(m*n)
    """
    
    def maxDotProduct(self, nums1, nums2):
        m, n = len(nums1), len(nums2)
        
        # Инициализация DP таблицы
        dp = [[-10**9] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                product = nums1[i - 1] * nums2[j - 1]
                
                # 4 варианта:
                # 1. Только текущее произведение
                # 2. Добавить к предыдущей подпоследовательности
                # 3. Пропустить элемент nums1
                # 4. Пропустить элемент nums2
                dp[i][j] = max(
                    product,
                    dp[i - 1][j - 1] + product,
                    dp[i - 1][j],
                    dp[i][j - 1]
                )
        
        return dp[m][n]