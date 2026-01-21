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

# from typing import List

class Solution:
    def minBitwiseArray(self, nums):
        ans = []
        
        for num in nums:
            result = -1
            
            # Попытаться снять один бит из num и проверить
            for bit in range(32):
                # Проверяем, установлен ли бит
                if (num & (1 << bit)) != 0:
                    # Попробуем это значение
                    candidate = num ^ (1 << bit)  # Снимаем бит
                    
                    # Проверяем условие: candidate | (candidate + 1) == num
                    if (candidate | (candidate + 1)) == num:
                        if result == -1 or candidate < result:
                            result = candidate
            
            ans.append(result)
        
        return ans