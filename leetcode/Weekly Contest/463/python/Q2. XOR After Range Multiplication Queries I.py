'''
https://leetcode.com/contest/weekly-contest-463/problems/xor-after-range-multiplication-queries-i/
'''

class Solution:
    def xorAfterQueries(self, a, q):
        M=1000000007
        for l,r,k,v in q:
            i=l
            while i<=r:
                a[i]=(a[i]*v)%M
                i+=k
        x=0
        for y in a:
            x^=y
        return x

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks