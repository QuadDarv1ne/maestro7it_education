/*
https://leetcode.com/contest/weekly-contest-464/problems/jump-game-ix/
*/

#define ll  long long 

class Solution {
public:
    vector<int> maxValue(vector<int>& nums) {
        
        int n = nums.size();
        vector<int> v = nums;
        int sz = 1;
        while (sz < n) sz <<= 1;
        const ll  I = 4000000000ll ;
        vector<long long> mn(2*sz, I);
        vector<long long> mx(2*sz, -I);
        
        for (int i=0;i<n;++i){ 
            mn[sz+i]=nums[i]; 
            mx[sz+i]=nums[i]; }

        
        for (int i=sz-1;i>0;--i){
            mn[i]=min(mn[i<<1],mn[i<<1|1]); 
            mx[i]=max(mx[i<<1],mx[i<<1|1]); }
        
        function<int(int,int,int,int,int,long long)> fl = [&](int idx,int l,int r,int ql,int qr,ll x)->int{
            if (ql>r||qr<l) return -1;
            if (mn[idx] >= x) return -1;
            if (l==r) return l;
            int m=(l+r)>>1;
            int t=fl(idx<<1,l,m,ql,qr,x);
            if (t!=-1) return t;
            return fl(idx<<1|1,m+1,r,ql,qr,x);
        };

        
        function<int(int,int,int,int,int,long long)> fg = [&](int idx,int l,int r,int ql,int qr,ll x)->int{
            if (ql>r||qr<l) return -1;
            if (mx[idx] <= x) return -1;
            if (l==r) return l;
            int m=(l+r)>>1;
            int t=fg(idx<<1,l,m,ql,qr,x);
            if (t!=-1) return t;
            return fg(idx<<1|1,m+1,r,ql,qr,x);
        };
        
        auto removeAt = [&](int p){
            int i = sz + p;
            mn[i]=I; mx[i]=-I;
            i >>= 1;
            while(i){
                mn[i]=min(mn[i<<1],mn[i<<1|1]);
                mx[i]=max(mx[i<<1],mx[i<<1|1]);
                i >>= 1;
            }
        };

        
        vector<char> vis(n,0);
        vector<int> ans(n,0);
        for (int s=0;s<n;++s){
            if (vis[s]) continue;
            vector<int> st;
            st.push_back(s);
            vis[s]=1;
            removeAt(s);
            vector<int> comp;
            comp.push_back(s);
            while(!st.empty()){
                int u = st.back(); st.pop_back();
                while(u+1 <= n-1){
                    int v = fl(1,0,sz-1,u+1,n-1, (long long)nums[u]);
                    if (v==-1) break;
                    if (!vis[v]){ vis[v]=1; removeAt(v); st.push_back(v); comp.push_back(v); }
                    else removeAt(v);
                }
                while(0 <= u-1){
                    int v = fg(1,0,sz-1,0,u-1, (long long)nums[u]);
                    if (v==-1) break;
                    if (!vis[v]){ vis[v]=1; removeAt(v); st.push_back(v); comp.push_back(v); }
                    else removeAt(v);
                }
            }
            
            int mval = nums[comp[0]];
            for (int x: comp) if (nums[x] > mval) mval = nums[x];
            for (int x: comp) ans[x] = mval;
        }

        
        return ans;
    }
};

/* Полезные ссылки: */
// 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
// 2. 💠Telegram №1💠 @quadd4rv1n7
// 3. 💠Telegram №2💠 @dupley_maxim_1999
// 4. Rutube канал: https://rutube.ru/channel/4218729/
// 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
// 6. YouTube канал: https://www.youtube.com/@it-coders
// 7. ВК группа: https://vk.com/science_geeks