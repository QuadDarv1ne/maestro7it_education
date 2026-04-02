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

Строит лексикографически наименьшую строку, удовлетворяющую условиям:
- Для каждого i, если str1[i] == 'T', то подстрока длины m начиная с i равна str2
- Если str1[i] == 'F', то эта подстрока не равна str2

Параметры:
    str1 (str): строка из 'T' и 'F' длины n
    str2 (str): целевая подстрока длины m

Возвращает:
    str: построенная строка длины n+m-1 или пустая строка, если решения нет
"""

class Solution(object):
    def generateString(self, str1, str2):
        """
        :type str1: str
        :type str2: str
        :rtype: str
        """
        n = len(str1)
        m = len(str2)
        length = n + m - 1
        
        # Инициализируем массив символов
        s = [''] * length
        
        # Сначала фиксируем все 'T' позиции
        for i in range(n):
            if str1[i] == 'T':
                for j in range(m):
                    idx = i + j
                    if s[idx] == '':
                        s[idx] = str2[j]
                    elif s[idx] != str2[j]:
                        return ""
        
        # Проверяем 'F' позиции
        for i in range(n):
            if str1[i] == 'F':
                # Проверяем, не получилось ли так, что эта подстрока всё равно равна str2
                match = True
                for j in range(m):
                    idx = i + j
                    if s[idx] == '':
                        match = False
                        break
                    if s[idx] != str2[j]:
                        match = False
                        break
                if match:
                    return ""
        
        # Заполняем оставшиеся позиции лексикографически наименьшими буквами
        # Для 'F' позиций нужно убедиться, что подстрока не равна str2
        # Мы будем использовать только 'a' и 'b' для минимизации
        
        # Сначала пробуем заполнить всё 'a'
        for i in range(length):
            if s[i] == '':
                s[i] = 'a'
        
        # Проверяем 'F' позиции
        for i in range(n):
            if str1[i] == 'F':
                # Проверяем, равна ли подстрока str2
                equal = True
                for j in range(m):
                    if s[i + j] != str2[j]:
                        equal = False
                        break
                if equal:
                    # Нужно изменить один символ
                    # Идём справа налево, чтобы минимизировать лексикографический порядок
                    changed = False
                    for j in range(m - 1, -1, -1):
                        idx = i + j
                        # Пробуем увеличить символ
                        if s[idx] < 'z':
                            s[idx] = chr(ord(s[idx]) + 1)
                            changed = True
                            break
                    if not changed:
                        return ""
        
        # Финальная проверка
        for i in range(n):
            substring = ''.join(s[i:i+m])
            if str1[i] == 'T' and substring != str2:
                return ""
            if str1[i] == 'F' and substring == str2:
                return ""
        
        return ''.join(s)