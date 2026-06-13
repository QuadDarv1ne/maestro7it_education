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
    def mapWordWeights(self, words, weights):
        result = []
        
        for word in words:
            total_weight = 0
            # Суммируем веса букв
            for char in word:
                index = ord(char) - ord('a')
                total_weight += weights[index]
            
            # Остаток от деления
            rem = total_weight % 26
            
            # Маппинг: 0 -> 'z', ..., 25 -> 'a'
            # Код 'z' минус остаток
            mapped_char = chr(ord('z') - rem)
            result.append(mapped_char)
            
        return "".join(result)