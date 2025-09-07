'''
https://leetcode.com/contest/weekly-contest-466/problems/count-binary-palindromic-numbers/description/
'''

class Solution:
    def countBinaryPalindromes(self, n: int) -> int:
        if n==0:return 1
        s=bin(n)[2:]
        L,r=len(s),1
        for l in range(1,L):
            if l==1: r+=1
            else:    r+=1<<(((l+1)//2)-1)

        h=(L+1)//2
        p,lo=int(s[:h],2),1<<(h-1)
        if p>lo:
            r+=p-lo

        t=s[:h]+(s[:h][:-1][::-1] if L&1 else s[:h][::-1])
        if t<=s:
            r+=1
        return r

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks