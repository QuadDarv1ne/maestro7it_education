/**
 * https://codeforces.com/contest/2136/problem/B
 */

// B_like_the_bitset.cpp
/*
B. Like the Bitset
Конструктивное решение: строим перестановку p[1..n] по колонкам i % k,
сначала заполняем '0' самыми большими числами, затем '1'. Затем верификация.
*/
#include <bits/stdc++.h>
using namespace std;
using vi = vector<int>;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if(!(cin >> t)) return 0;
    while(t--){
        int n,k;
        string s;
        cin >> n >> k >> s;
        if(k == 1 && s.find('1') != string::npos){
            cout << "NO\n";
            continue;
        }
        vector<vector<int>> cols(k);
        for(int i=0;i<n;i++){
            cols[i % k].push_back(i);
        }
        vector<int> p(n, 0);
        int cur = n;
        for(int r=0;r<k;r++){
            vector<int> zeros, ones;
            for(int idx: cols[r]){
                if(s[idx] == '0') zeros.push_back(idx);
                else ones.push_back(idx);
            }
            for(int idx: zeros) p[idx] = cur-- ;
            for(int idx: ones) p[idx] = cur-- ;
        }
        // Верификация: для каждого окна дли k вычислим максимум
        bool valid = true;
        if(k <= n){
            deque<int> dq;
            vector<int> winmax(n - k + 1);
            for(int i=0;i<n;i++){
                while(!dq.empty() && p[dq.back()] <= p[i]) dq.pop_back();
                dq.push_back(i);
                if(dq.front() <= i - k) dq.pop_front();
                if(i >= k-1) winmax[i - k + 1] = p[dq.front()];
            }
            for(int i=0;i<n;i++){
                if(s[i] == '1'){
                    int L = max(0, i - k + 1);
                    int R = min(i, n - k);
                    for(int st = L; st <= R; ++st){
                        if(winmax[st] == p[i]){
                            valid = false;
                            break;
                        }
                    }
                    if(!valid) break;
                }
            }
        }
        if(!valid){
            cout << "NO\n";
        } else {
            cout << "YES\n";
            for(int i=0;i<n;i++){
                if(i) cout << ' ';
                cout << p[i];
            }
            cout << '\n';
        }
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