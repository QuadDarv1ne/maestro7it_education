'''
https://leetcode.com/problems/word-ladder/description/?envType=study-plan-v2&envId=top-interview-150
'''

from collections import deque

class Solution:
    def ladderLength(self, beginWord, endWord, wordList):
        wordDict = set(wordList)
        if endWord not in wordDict:
            return 0

        queue = deque([(beginWord, 1)])

        while queue:
            current_word, level = queue.popleft()

            for i in range(len(current_word)):
                for char in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = current_word[:i] + char + current_word[i+1:]
                    if next_word == endWord:
                        return level + 1
                    if next_word in wordDict:
                        wordDict.remove(next_word)
                        queue.append((next_word, level + 1))

        return 0

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks