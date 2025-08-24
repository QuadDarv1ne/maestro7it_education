'''
https://leetcode.com/contest/weekly-contest-464/problems/maximum-walls-destroyed-by-robots/description/
'''

class Solution:
    def maxWalls(self, r, d, w):
        def c(L,R):
            if L>R:
                return 0
            return bisect_right(w,R)-bisect_left(w,L)

        if not w: return 0
        z=sorted(zip(r,d))
        r=[p for p,_ in z]
        d=[q for _,q in z]

        w=sorted(w)
        n=len(r)
        cl,cr=[0]*n,[0]*n
        Ls,Rs=[(0, -1)]*n,[(0, -1)]*n
        Ls[0]=(r[0]-d[0], r[0])
        cl[0]=c(Ls[0][0],Ls[0][1])
        for i in range(1,n):
            L=max(r[i]-d[i], r[i-1]+1)
            U=r[i]
            Ls[i]=(L,U)
            cl[i]=c(L,U)

        for i in range(n-1):
            L=r[i]
            U=min(r[i]+d[i], r[i+1]-1)
            Rs[i]=(L,U)
            cr[i]=c(L,U)

        Rs[n-1]=(r[n-1], r[n-1]+d[n-1])
        cr[n-1]=c(Rs[n-1][0],Rs[n-1][1])
        cu=[0]*(n-1)
        for i in range(n-1):
            aL,aU=Rs[i]
            bL,bU=Ls[i+1]
            if aL>aU and bL>bU: cu[i]=0
            elif aL>aU: cu[i]=cl[i+1]
            elif bL>bU: cu[i]=cr[i]
            else:
                s=aL if aL>bL else bL
                t=aU if aU<bU else bU
                ov=c(s,t) if s<=t else 0
                cu[i]=cr[i]+cl[i+1]-ov

        dl,dr=cl[0],0
        for i in range(n-1):
            nl=dr+cu[i] if dr+cu[i]>dl+cl[i+1] else dl+cl[i+1]
            nr=dr+cr[i] if dr+cr[i]>dl else dl
            dl,nr=nl,nr
            dr=nr

        res=dr+cr[n-1] if dr+cr[n-1]>dl else dl
        return res

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks