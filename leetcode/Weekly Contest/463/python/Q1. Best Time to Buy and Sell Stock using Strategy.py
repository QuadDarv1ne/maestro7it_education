'''
https://leetcode.com/contest/weekly-contest-463/problems/best-time-to-buy-and-sell-stock-using-strategy/
'''

class Solution:
    def maxProfit(self, p, s, k):
        n=len(p); h=k//2
        pp=[0]*(n+1); pc=[0]*(n+1)
        t=0
        for i in range(n):
            pp[i+1]=pp[i]+p[i]
            v=s[i]*p[i]
            pc[i+1]=pc[i]+v
            t+=v
        b=-inf; e=n-k; i=0
        while i<=e:
            d=(pp[i+k]-pp[i+h])-(pc[i+k]-pc[i])
            if b<d: b=d
            i+=1
        if b>0: t+=b
        return t

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks