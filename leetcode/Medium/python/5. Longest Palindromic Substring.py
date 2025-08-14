'''
https://leetcode.com/problems/longest-palindromic-substring/description/
'''

class Solution:
    def longestPalindrome(self, s):
        """
        Находит самую длинную палиндромную подстроку в s.
        
        Алгоритм:
        - Расширяем палиндром из каждого символа или между символами.
        - Для каждого индекса проверяем:
          * Нечётный палиндром (центр один символ)
          * Чётный палиндром (центр между символами)
        - Возвращаем самую длинную найденную подстроку.
        """
        if not s:
            return ""
        
        def expand_around_center(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left + 1:right]
        
        longest = ""
        for i in range(len(s)):
            odd = expand_around_center(i, i)
            even = expand_around_center(i, i + 1)
            longest = max(longest, odd, even, key=len)
        return longest

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks