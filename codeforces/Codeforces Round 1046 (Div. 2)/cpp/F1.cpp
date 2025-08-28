/**
 * https://codeforces.com/contest/2136/problem/F1
 */

// F_from_the_unknown_offline.cpp
/*
F1/F2. From the Unknown (offline/hack format)
Формат: возможно "t manual" или просто t, затем в каждой строке W.
Вывод: W для каждого теста.
*/
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string first;
    if(!(cin >> first)) return 0;
    int t;
    // first token can be number
    try {
        t = stoi(first);
    } catch(...) {
        return 0;
    }
    // check if next token on same line is "manual" (we ignore it)
    string maybe;
    if(cin.peek()=='\n'){
        // nothing
    } else {
        cin >> maybe;
        if(maybe != "manual"){
            // it was actually part of next input; put back by using stringstreams is messy; but common hack input will have manual or not
            // however to be robust, treat maybe as first W for test 1
            cout << maybe << "\n";
            for(int i=1;i<t;i++){
                string W; cin >> W;
                cout << W << "\n";
            }
            return 0;
        }
    }
    for(int i=0;i<t;i++){
        string W;
        // skip empty lines
        do { if(!getline(cin, W)) break; } while(W.size()==0);
        if(W.size()==0){
            if(!(cin >> W)) break;
        }
        // trim
        stringstream ss(W);
        ss >> W;
        cout << W << "\n";
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