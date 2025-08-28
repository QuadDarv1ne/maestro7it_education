/**
 * https://codeforces.com/contest/2136/problem/A
 */

// A_in_the_dream.cpp
/*
A. In the Dream
Проверяет, возможно ли соблюдение условия: в каждой половине матча
запрещено иметь три подряд голов одной команды.
Вход: t тестов, в каждом a b c d
Выход: YES или NO
*/
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int max_allowed(int L){
    return (2*L + 2) / 3; // ceil(2L/3)
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if(!(cin >> t)) return 0;
    while(t--){
        int a,b,c,d;
        cin >> a >> b >> c >> d;
        bool ok = true;
        int L1 = a + b;
        if(max(a,b) > max_allowed(L1)) ok = false;
        int L2 = (c - a) + (d - b);
        if(max(c-a, d-b) > max_allowed(L2)) ok = false;
        cout << (ok ? "YES" : "NO") << '\n';
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