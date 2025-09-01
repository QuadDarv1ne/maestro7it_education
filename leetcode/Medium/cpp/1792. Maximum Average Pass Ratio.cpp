/**
 * https://leetcode.com/problems/maximum-average-pass-ratio/description/?envType=daily-question&envId=2025-09-01
 */

// C++17 — LeetCode
// Используем priority_queue с кортежем (gain, p, t). priority_queue по умолчанию — max-heap.
#include <vector>
#include <queue>
#include <tuple>
using namespace std;

double gain(int p, int t) {
    return double(p + 1) / double(t + 1) - double(p) / double(t);
}

class Solution {
public:
    double maxAverageRatio(vector<vector<int>>& classes, int extraStudents) {
        priority_queue<tuple<double,int,int>> pq;
        for (auto &c : classes) {
            int p = c[0], t = c[1];
            pq.emplace(gain(p,t), p, t);
        }
        while (extraStudents--) {
            auto [g, p, t] = pq.top(); pq.pop();
            ++p; ++t;
            pq.emplace(gain(p,t), p, t);
        }
        double sum = 0.0;
        while (!pq.empty()) {
            auto [g, p, t] = pq.top(); pq.pop();
            sum += double(p) / double(t);
        }
        return sum / classes.size();
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