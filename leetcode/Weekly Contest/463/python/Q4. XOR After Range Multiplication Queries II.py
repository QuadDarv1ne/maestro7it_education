'''
https://leetcode.com/contest/weekly-contest-463/problems/xor-after-range-multiplication-queries-ii/
'''

class Solution:
    def xorAfterQueries(self, a, q):
        M=1000000007
        n=len(a)
        b=int(n**0.5)+1
        d={}; inv={}
        for l,r,k,v in q:
            if k>=b:
                i=l
                while i<=r:
                    a[i]=(a[i]*v)%M; i+=k
            else:
                c=l%k
                key=(k,c)
                if key not in d:d[key]={}
                tl=(l-c)//k; tr=(r-c)//k
                e=d[key]; u=inv.get(v)
                if u is None:
                    u=pow(v,M-2,M); inv[v]=u
                e[tl]=(e.get(tl,1)*v)%M
                x=tr+1
                e[x]=(e.get(x,1)*u)%M
        for (k,c),e in d.items():
            if c>=n: continue
            L=(n-1-c)//k+1
            cur=1
            for t in range(L):
                cur=(cur*e.get(t,1))%M
                i=c+t*k
                a[i]=(a[i]*cur)%M
        x=0
        for v in a: x^=v
        return x

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks