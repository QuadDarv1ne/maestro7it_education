'''
https://leetcode.com/problems/vowel-spellchecker/description/?envType=daily-question&envId=2025-09-14
'''

class Solution:
    """Решение задачи Vowel Spellchecker.

    Для каждого запроса из queries ищем слово в wordlist по следующим правилам:
    1. Точное совпадение.
    2. Совпадение без учета регистра (первое найденное).
    3. Совпадение с заменой всех гласных на '*' (первое найденное).
    4. Если ничего не найдено, возвращаем пустую строку.
    """
    def spellchecker(self, wordlist: List[str], queries: List[str]) -> List[str]:
        # Создаем множество для точных совпадений
        exact = set(wordlist)
        # Словарь для регистра-независимого поиска: ключ — слово в нижнем регистре, значение — первое слово из wordlist
        case_insensitive = {}
        # Словарь для поиска с заменой гласных на '*': ключ — строка с замененными гласными, значение — первое слово
        vowel_insensitive = {}
        
        for word in wordlist:
            lower = word.lower()
            # Если в case_insensitive еще нет этого нижнего регистра, добавляем
            if lower not in case_insensitive:
                case_insensitive[lower] = word
            # Создаем ключ для гласных замены: заменяем все гласные на '*'
            # Используем translate для удобства
            vowel_key = lower.translate(str.maketrans('aeiou', '*****'))
            if vowel_key not in vowel_insensitive:
                vowel_insensitive[vowel_key] = word
        
        res = []
        for query in queries:
            # Проверяем точное совпадение
            if query in exact:
                res.append(query)
                continue
            lower_query = query.lower()
            # Проверяем регистра-независимое совпадение
            if lower_query in case_insensitive:
                res.append(case_insensitive[lower_query])
                continue
            # Заменяем гласные в lower_query на '*' и проверяем
            vowel_query = lower_query.translate(str.maketrans('aeiou', '*****'))
            if vowel_query in vowel_insensitive:
                res.append(vowel_insensitive[vowel_query])
            else:
                res.append('')
        return res

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks