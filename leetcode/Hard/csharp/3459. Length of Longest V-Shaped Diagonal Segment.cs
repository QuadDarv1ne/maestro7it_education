/**
 * https://leetcode.com/problems/length-of-longest-v-shaped-diagonal-segment/description/?envType=daily-question&envId=2025-08-27
 */

public class Solution {
    /**
     * В матрице grid нужно найти длину самого длинного "V-образного"
     * диагонального сегмента.
     * Сегмент начинается с 1, далее идёт шаблон 2-0-2-0,
     * разрешён один поворот на 90° по часовой стрелке.
     */
    public int LenOfVDiagonal(int[][] grid) {
        int n = grid.Length, m = grid[0].Length;
        int[][][] end = new int[4][][];
        int[][][] go = new int[4][][];
        for (int d=0; d<4; d++) {
            end[d]=new int[n][]; go[d]=new int[n][];
            for (int i=0;i<n;i++) {
                end[d][i]=new int[m];
                go[d][i]=new int[m];
                for (int j=0;j<m;j++) go[d][i][j]=1;
            }
        }

        (int,int)[] dirs = {(1,1),(-1,1),(1,-1),(-1,-1)};
        int[] cw={2,0,3,1};

        Func<int,int,bool> ok = (a,b)=>{
            if (a==1) return b==2;
            if (a==2) return b==0;
            if (a==0) return b==2;
            return false;
        };

        // end
        for (int d=0; d<4; d++) {
            int dx=dirs[d].Item1,dy=dirs[d].Item2;
            var xs=Enumerable.Range(0,n).ToList();
            var ys=Enumerable.Range(0,m).ToList();
            if (dx==-1) xs.Reverse();
            if (dy==-1) ys.Reverse();
            foreach (int i in xs) foreach (int j in ys) {
                int val=grid[i][j];
                int pi=i-dx,pj=j-dy;
                if (pi>=0&&pi<n&&pj>=0&&pj<m && ok(grid[pi][pj],val) && end[d][pi][pj]>0)
                    end[d][i][j]=end[d][pi][pj]+1;
                else end[d][i][j]=(val==1?1:0);
            }
        }

        // go
        for (int d=0; d<4; d++) {
            int dx=dirs[d].Item1,dy=dirs[d].Item2;
            var xs=Enumerable.Range(0,n).ToList();
            var ys=Enumerable.Range(0,m).ToList();
            if (dx==1) xs.Reverse();
            if (dy==1) ys.Reverse();
            foreach (int i in xs) foreach (int j in ys) {
                int ni=i+dx,nj=j+dy;
                if (ni>=0&&ni<n&&nj>=0&&nj<m && ok(grid[i][j],grid[ni][nj]))
                    go[d][i][j]=1+go[d][ni][nj];
                else go[d][i][j]=1;
            }
        }

        int ans=0;
        for (int d=0;d<4;d++) for (int i=0;i<n;i++) for (int j=0;j<m;j++)
            ans=Math.Max(ans,end[d][i][j]);

        for (int i=0;i<n;i++) for (int j=0;j<m;j++) for (int a=0;a<4;a++) {
            int b=cw[a];
            if (end[a][i][j]>0)
                ans=Math.Max(ans,end[a][i][j]+go[b][i][j]-1);
        }
        return ans;
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/