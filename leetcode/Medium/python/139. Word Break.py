'''
https://leetcode.com/problems/word-break/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution(object):
    def wordBreak(self, s, wordDict):
        """
        Определяет, можно ли строку s разбить на последовательность слов из словаря wordDict.

        :param s: Исходная строка
        :param wordDict: Список слов словаря
        :return: True, если строку можно разбить, иначе False
        """
        wordSet = set(wordDict)
        dp = [False] * (len(s) + 1)
        dp[0] = True  # Пустая строка всегда может быть разбита

        for i in range(1, len(s) + 1):
            for j in range(i):
                if dp[j] and s[j:i] in wordSet:
                    dp[i] = True
                    break

        return dp[len(s)]

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks