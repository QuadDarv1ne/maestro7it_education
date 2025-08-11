'''
https://leetcode.com/problems/text-justification/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution:
    def fullJustify(self, words, maxWidth):
        """
        Форматирует список слов в полностью выровненный по ширине текст.

        Задача:
        - Составить строки длиной ровно maxWidth символов.
        - Распределить пробелы между словами максимально равномерно.
        - Если пробелы распределяются неравномерно, более "широкие" пробелы
          должны идти в начале строки.
        - Последняя строка всегда выравнивается по левому краю (слова через один пробел, остаток пробелами справа).

        Параметры:
        ----------
        words : List[str]
            Список слов (длина каждого > 0 и ≤ maxWidth).
        maxWidth : int
            Желаемая длина каждой строки.

        Возвращает:
        -----------
        List[str]
            Список строк, каждая ровно maxWidth символов, с полным выравниванием.

        Алгоритм:
        1. С помощью жадного подхода набираем слова в текущую строку,
           пока они помещаются по длине (учитывая пробелы между ними).
        2. Когда строка "заполнена", распределяем пробелы:
            - если строка последняя или в ней одно слово — выравнивание влево;
            - иначе распределяем пробелы равномерно, остаток в начале.
        3. Продолжаем, пока не обработаем все слова.

        Сложность:
        ----------
        O(N) по времени, где N — общее количество символов во входных словах.
        O(1) по дополнительной памяти (не считая результата).
        """
        res = []
        i = 0
        n = len(words)

        while i < n:
            length = len(words[i])
            j = i + 1
            # Подбираем слова, которые войдут в строку
            while j < n and length + 1 + len(words[j]) <= maxWidth:
                length += 1 + len(words[j])
                j += 1

            line = ""
            numWords = j - i

            # Последняя строка или одна строка — выравнивание влево
            if j == n or numWords == 1:
                line = " ".join(words[i:j])
                line += " " * (maxWidth - len(line))
            else:
                totalSpaces = maxWidth - sum(len(word) for word in words[i:j])
                spaceBetween = totalSpaces // (numWords - 1)
                extraSpaces = totalSpaces % (numWords - 1)

                for k in range(numWords - 1):
                    line += words[i + k]
                    line += " " * (spaceBetween + (1 if k < extraSpaces else 0))
                line += words[j - 1]

            res.append(line)
            i = j

        return res

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks