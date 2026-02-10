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
    def hIndex(self, citations):
        """
        Находит h-индекс из отсортированного массива цитирований.
        
        H-индекс: максимальное число h, такое что исследователь имеет
        как минимум h статей, каждая из которых цитируется как минимум h раз.
        
        Args:
            citations: Отсортированный массив цитирований (по возрастанию)
            
        Returns:
            h-индекс
            
        Примеры:
            >>> hIndex([0,1,3,5,6])
            3
            >>> hIndex([1,2,100])
            2
            
        Сложность:
            Время: O(log n)
            Память: O(1)
        """
        n = len(citations)
        left, right = 0, n - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            # Количество статей с цитированиями >= citations[mid]
            papers = n - mid
            
            if citations[mid] >= papers:
                # Можем попробовать найти большее h
                right = mid - 1
            else:
                # Нужно больше цитирований
                left = mid + 1
                
        return n - left