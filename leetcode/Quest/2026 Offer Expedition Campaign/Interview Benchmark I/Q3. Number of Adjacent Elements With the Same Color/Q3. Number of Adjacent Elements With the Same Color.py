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

class Solution:
    def colorTheArray(self, n, queries):
        colors = [0] * n
        count = 0
        result = []
        
        for i, color in queries:
            old = colors[i]
            if old == color:
                result.append(count)
                continue
            
            # Undo old color's contributions
            if i > 0 and colors[i-1] != 0 and colors[i-1] == old:
                count -= 1
            if i < n-1 and colors[i+1] != 0 and colors[i+1] == old:
                count -= 1
            
            # Update color
            colors[i] = color
            
            # Add new color's contributions
            if i > 0 and colors[i-1] != 0 and colors[i-1] == color:
                count += 1
            if i < n-1 and colors[i+1] != 0 and colors[i+1] == color:
                count += 1
            
            result.append(count)
        
        return result