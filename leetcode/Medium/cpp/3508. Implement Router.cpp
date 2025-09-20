/**
 * https://leetcode.com/problems/implement-router/description/?envType=daily-question&envId=2025-09-20
 */

#include <bits/stdc++.h>
using namespace std;

class Router {
    int memoryLimit;
    queue<tuple<int,int,int>> q;   // FIFO очередь
    unordered_set<string> seen;    // уникальные пакеты
    unordered_map<int, vector<int>> destMap;
    unordered_map<int, int> startIndex;

    string makeKey(int s, int d, int t) {
        return to_string(s) + "#" + to_string(d) + "#" + to_string(t);
    }

public:
    Router(int memoryLimit): memoryLimit(memoryLimit) {}

    bool addPacket(int source, int destination, int timestamp) {
        string key = makeKey(source, destination, timestamp);
        if (seen.count(key)) return false;
        if ((int)q.size() == memoryLimit) forwardPacket();
        q.emplace(source, destination, timestamp);
        seen.insert(key);
        destMap[destination].push_back(timestamp);
        return true;
    }

    vector<int> forwardPacket() {
        if (q.empty()) return {};
        auto [s,d,t] = q.front(); q.pop();
        string key = makeKey(s,d,t);
        seen.erase(key);
        if (destMap[d][startIndex[d]] == t)
            startIndex[d]++;
        return {s,d,t};
    }

    int getCount(int destination, int startTime, int endTime) {
        auto &arr = destMap[destination];
        int start = startIndex[destination];
        auto L = lower_bound(arr.begin()+start, arr.end(), startTime);
        auto R = upper_bound(arr.begin()+start, arr.end(), endTime);
        return R - L;
    }
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/