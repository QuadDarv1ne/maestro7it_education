/**
 * https://codeforces.com/contest/2136/problem/C
 */

// C_against_the_difference.cpp
/*
C. Against the Difference
Для каждого значения v можно взять floor(cnt[v] / v) полных блоков длины v.
Суммируем v * (cnt[v] / v).
*/
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if(!(cin >> t)) return 0;
    while(t--){
        int n; cin >> n;
        unordered_map<int,int> cnt;
        cnt.reserve(n*2);
        for(int i=0;i<n;i++){
            int x; cin >> x;
            cnt[x]++;
        }
        long long ans = 0;
        for(auto &kv: cnt){
            long long v = kv.first;
            long long c = kv.second;
            ans += v * (c / v);
        }
        cout << ans << '\n';
    }
    return 0;
}

/** Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
*/