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
    def spellchecker(self, wordlist, queries):
        exact = set(wordlist)
        case_insensitive = {}
        vowel_insensitive = {}
        
        for word in wordlist:
            lower = word.lower()
            if lower not in case_insensitive:
                case_insensitive[lower] = word
            vowel_key = ''.join('*' if c in 'aeiou' else c for c in lower)
            if vowel_key not in vowel_insensitive:
                vowel_insensitive[vowel_key] = word
        
        res = []
        for query in queries:
            if query in exact:
                res.append(query)
                continue
            lower_query = query.lower()
            if lower_query in case_insensitive:
                res.append(case_insensitive[lower_query])
                continue
            vowel_query = ''.join('*' if c in 'aeiou' else c for c in lower_query)
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