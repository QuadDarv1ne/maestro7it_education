"""
https://leetcode.com/problems/check-if-strings-can-be-made-equal-with-operations-ii/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "2840. Check if Strings Can be Made Equal With Operations II" на Python

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
    def checkStrings(self, s1, s2):
        if len(s1) != len(s2):
            return False
            
        even = [0] * 26
        odd = [0] * 26
        
        for i in range(len(s1)):
            if i % 2 == 0:
                even[ord(s1[i]) - ord('a')] += 1
                even[ord(s2[i]) - ord('a')] -= 1
            else:
                odd[ord(s1[i]) - ord('a')] += 1
                odd[ord(s2[i]) - ord('a')] -= 1
                
        return all(c == 0 for c in even) and all(c == 0 for c in odd)