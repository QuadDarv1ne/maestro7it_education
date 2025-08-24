'''
https://leetcode.com/contest/weekly-contest-464/
'''

class Solution:
    def maxValue(self, a):
        n=len(a)
        if n==0: return []
        if n==1: return [a[0]]
        p=[0]*n
        p[0]=a[0]
        for i in range(1,n):
            t=p[i-1]
            p[i]=t if t>=a[i] else a[i]
        s=[0]*n
        s[-1]=a[-1]
        for i in range(n-2,-1,-1):
            t=s[i+1]
            s[i]=t if t<=a[i] else a[i]
        r=[0]*n
        st=0
        for i in range(n-1):
            if p[i]<=s[i+1]:
                m=p[i]
                for j in range(st,i+1):
                    r[j]=m
                st=i+1
        m=p[-1]
        for j in range(st,n):
            r[j]=m
        return r

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks