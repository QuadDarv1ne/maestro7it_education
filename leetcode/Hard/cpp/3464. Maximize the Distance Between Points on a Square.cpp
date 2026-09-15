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

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxDistance(int side, vector<vector<int>>& points, int k) {
        int n = points.size();
        vector<long long> pos(n);
        // Преобразование границы в 1D координату (обход по часовой стрелке)
        for (int i = 0; i < n; ++i) {
            int x = points[i][0], y = points[i][1];
            if (y == 0) pos[i] = x;                      // нижняя грань
            else if (x == side) pos[i] = (long long)side + y; // правая грань
            else if (y == side) pos[i] = 2LL * side + (side - x); // верхняя грань
            else pos[i] = 3LL * side + (side - y);            // левая грань
        }
        sort(pos.begin(), pos.end());

        long long perimeter = 4LL * side;
        // Дублируем массив для удобства обработки цикличности
        vector<long long> extended(2 * n);
        for (int i = 0; i < n; ++i) {
            extended[i] = pos[i];
            extended[i + n] = pos[i] + perimeter;
        }

        long long low = 0, high = 2LL * side, ans = 0;
        // Бинарный поиск по ответу
        while (low <= high) {
            long long mid = (low + high) / 2;
            if (canPlace(extended, n, k, mid, perimeter)) {
                ans = mid;
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return ans;
    }

private:
    bool canPlace(const vector<long long>& extended, int n, int k,
                  long long d, long long perimeter) {
        // Перебираем каждую точку как стартовую
        for (int start = 0; start < n; ++start) {
            int cnt = 1;
            long long lastPos = extended[start];
            int curIdx = start;

            // Жадно выбираем следующие точки
            while (cnt < k) {
                // Ищем первую позицию >= lastPos + d
                long long target = lastPos + d;
                auto it = lower_bound(extended.begin() + curIdx + 1,
                                      extended.begin() + start + n,
                                      target);
                if (it == extended.begin() + start + n) break;
                curIdx = it - extended.begin();
                lastPos = *it;
                ++cnt;
            }

            // Убеждаемся, что циклическое расстояние от последней до стартовой также >= d
            if (cnt == k && extended[start] + perimeter - lastPos >= d)
                return true;
        }
        return false;
    }
};