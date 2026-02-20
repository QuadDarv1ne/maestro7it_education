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
    def makeLargestSpecial(self, s):
        """
        Преобразует специальную двоичную строку в лексикографически наибольшую.
        
        Параметры:
        s (str): исходная специальная строка (например, "11011000").
        
        Возвращает:
        str: максимально возможная строка после перестановок (например, "11100100").
        """
        def dfs(s):
            # Базовый случай: пустая строка
            if not s:
                return ""
            
            groups = []          # Список для хранения обработанных подстрок текущего уровня
            balance = 0           # Текущий баланс (разность количества единиц и нулей)
            left = 0              # Начало текущей группы
            
            for i, ch in enumerate(s):
                balance += 1 if ch == '1' else -1
                # Когда баланс становится нулевым, мы нашли группу s[left:i+1]
                if balance == 0:
                    # Обрабатываем внутренность без первого ('1') и последнего ('0') символов
                    inner = dfs(s[left+1:i])
                    groups.append('1' + inner + '0')
                    left = i + 1   # Сдвигаем начало для следующей группы
            
            # Сортируем группы по убыванию (лексикографически)
            groups.sort(reverse=True)
            return ''.join(groups)
        
        return dfs(s)