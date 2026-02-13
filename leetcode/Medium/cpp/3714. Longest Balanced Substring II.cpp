/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
using namespace std;

class Solution {
public:
    int longestBalanced(string s) {
        int n = s.size();
        int ans = 0;

        // ---------- Случай 1: один символ ----------
        for (char ch : {'a', 'b', 'c'}) {
            int cur = 0;
            for (char c : s) {
                if (c == ch) cur++;
                else cur = 0;
                ans = max(ans, cur);
            }
        }

        // ---------- Случай 2: ровно два символа ----------
        vector<pair<char,char>> pairs = {{'a','b'}, {'a','c'}, {'b','c'}};
        for (auto [x, y] : pairs) {
            char third = 'a' + 'b' + 'c' - x - y; // третий символ (разделитель)
            vector<string> segments;
            size_t start = 0, end;
            while ((end = s.find(third, start)) != string::npos) {
                if (end > start) segments.push_back(s.substr(start, end - start));
                start = end + 1;
            }
            if (start < s.size()) segments.push_back(s.substr(start));

            for (const string& seg : segments) {
                int m = seg.size();
                if (m < 2) continue;
                vector<int> prefX(m + 1, 0), prefY(m + 1, 0);
                for (int i = 0; i < m; ++i) {
                    prefX[i + 1] = prefX[i] + (seg[i] == x ? 1 : 0);
                    prefY[i + 1] = prefY[i] + (seg[i] == y ? 1 : 0);
                }
                unordered_map<int, int> firstOcc;
                int diff = 0;
                firstOcc[0] = 0;
                for (int i = 1; i <= m; ++i) {
                    if (seg[i - 1] == x) diff++;
                    else if (seg[i - 1] == y) diff--;
                    if (firstOcc.count(diff)) {
                        int startIdx = firstOcc[diff];
                        if (prefX[i] - prefX[startIdx] > 0 && prefY[i] - prefY[startIdx] > 0) {
                            ans = max(ans, i - startIdx);
                        }
                    } else {
                        firstOcc[diff] = i;
                    }
                }
            }
        }

        // ---------- Случай 3: три символа ----------
        unordered_map<int, unordered_map<int, pair<int, tuple<int,int,int>>>> firstOcc3;
        // Ключ: (d_b, d_c) -> (индекс, cntA, cntB, cntC)
        // Для удобства храним как вложенные map, либо преобразуем в строку. 
        // Но проще использовать map с ключом как пара.
        // В C++ удобно: map<pair<int,int>, tuple<int,int,int,int>>
        map<pair<int,int>, tuple<int,int,int,int>> occ;
        occ[{0,0}] = {-1, 0,0,0};
        int cntA = 0, cntB = 0, cntC = 0;
        for (int i = 0; i < n; ++i) {
            if (s[i] == 'a') cntA++;
            else if (s[i] == 'b') cntB++;
            else cntC++;
            pair<int,int> key = {cntB - cntA, cntC - cntA};
            if (occ.count(key)) {
                auto [idx, sa, sb, sc] = occ[key];
                if (cntA - sa > 0 && cntB - sb > 0 && cntC - sc > 0) {
                    ans = max(ans, i - idx);
                }
            } else {
                occ[key] = {i, cntA, cntB, cntC};
            }
        }

        return ans;
    }
};