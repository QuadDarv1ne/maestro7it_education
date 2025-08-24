'''
https://leetcode.com/contest/weekly-contest-463/problems/minimum-sum-after-divisible-sum-deletions/
'''

class Solution:
    def minArraySum(self, a, k):
        t=0
        for x in a: t+=x
        b=[-inf]*k
        b[0]=0
        d=0
        p=0
        for x in a:
            p+=x
            r=p%k
            v=b[r]+p
            if d<v: d=v
            w=d-p
            if b[r]<w: b[r]=w
        return t-d

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks