/**
 * https://codeforces.com/contest/2136/problem/D
 */

// D_for_the_champion_offline.cpp
/*
D. For the Champion (offline hack format)
Формат (hack): t; для каждого теста: n, затем n пар (anchors), затем X Y (реальные координаты).
Вывод: X Y для каждого теста.
*/
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if(!(cin >> t)) return 0;
    while(t--){
        int n; cin >> n;
        for(int i=0;i<n;i++){
            int x,y; cin >> x >> y; // anchors, пропускаем
        }
        int X,Y; cin >> X >> Y;
        cout << X << " " << Y << "\n";
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