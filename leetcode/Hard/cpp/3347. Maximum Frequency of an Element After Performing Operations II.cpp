/*
Задача: Maximum Frequency of an Element After Performing Operations II
Источник: https://leetcode.com/problems/maximum-frequency-of-an-element-after-performing-operations-ii/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

class Solution {
public:
    // Сигнатура: vector<int>& nums, int k, int numOperations
    int maxFrequency(vector<int>& nums, int k, int numOperations) {
        if (nums.empty()) return 0;

        int n = nums.size();
        // переводим в long long для безопасных арифметических операций
        vector<ll> a(nums.begin(), nums.end());
        sort(a.begin(), a.end());

        unordered_map<ll,int> freq;
        freq.reserve(n * 2);
        for (ll x : a) freq[x]++;

        int ans = 1;

        // 1) Для каждого существующего значения v считаем, сколько элементов попадает в [v-k, v+k]
        vector<ll> unique_vals;
        unique_vals.reserve(freq.size());
        for (auto &p : freq) unique_vals.push_back(p.first);
        sort(unique_vals.begin(), unique_vals.end());

        for (ll v : unique_vals) {
            ll leftVal = v - (ll)k;
            ll rightVal = v + (ll)k;
            auto itL = lower_bound(a.begin(), a.end(), leftVal);
            auto itR = upper_bound(a.begin(), a.end(), rightVal);
            int cover = int(itR - itL);
            int candidate = min(cover, freq[v] + numOperations);
            ans = max(ans, candidate);
        }

        // 2) Sweep по интервалам [a-k, a+k] — найти точку с максимальным покрытием
        vector<pair<ll,int>> events;
        events.reserve(2 * n);
        for (ll x : a) {
            events.emplace_back(x - (ll)k, 1);
            events.emplace_back(x + (ll)k + 1, -1); // end inclusive -> decrement at end+1
        }
        sort(events.begin(), events.end());
        int cur = 0;
        int max_cover = 0;
        for (auto &ev : events) {
            cur += ev.second;
            max_cover = max(max_cover, cur);
        }

        int candidate2 = min(max_cover, numOperations);
        ans = max(ans, candidate2);

        return ans;
    }
};

/*
Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
8. Официальный сайт школы Maestro7IT: https://school-maestro7it.ru/
*/