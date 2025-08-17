'''
https://leetcode.com/problems/validate-ip-address/description/
'''

import re

class Solution:
    def validIPAddress(self, queryIP):
        """
        Проверяет, является ли строка queryIP допустимым IPv4 или IPv6 адресом.

        Алгоритм:
        1. Если строка содержит точку ('.'), проверяем как IPv4.
        2. Если строка содержит двоеточие (':'), проверяем как IPv6.
        3. Если строка не содержит ни того, ни другого, возвращаем 'Neither'.

        Время: O(n), где n — длина строки queryIP.
        Память: O(1).
        """
        # Проверка на IPv4
        if '.' in queryIP:
            parts = queryIP.split('.')
            if len(parts) == 4:
                for part in parts:
                    if not part.isdigit() or not 0 <= int(part) <= 255 or (part[0] == '0' and len(part) > 1):
                        return "Neither"
                return "IPv4"
        
        # Проверка на IPv6
        elif ':' in queryIP:
            parts = queryIP.split(':')
            if len(parts) == 8:
                for part in parts:
                    if not (1 <= len(part) <= 4) or not all(c in '0123456789abcdefABCDEF' for c in part):
                        return "Neither"
                return "IPv6"
        
        return "Neither"

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks