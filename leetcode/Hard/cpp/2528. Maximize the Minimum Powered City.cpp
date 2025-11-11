/*
https://leetcode.com/problems/maximize-the-minimum-powered-city/?envType=daily-question&envId=2025-11-07

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
public:
    long long maxPower(vector<int>& stations, int r, int k) {
        int n = stations.size();
        vector<long long> diff(n + 1, 0);
        
        // Построение начального diff-массива
        for (int i = 0; i < n; ++i) {
            int left = max(0, i - r);
            int right = min(n - 1, i + r);
            diff[left] += stations[i];
            diff[right + 1] -= stations[i];
        }
        
        // Восстановление power[i]
        vector<long long> power(n);
        power[0] = diff[0];
        for (int i = 1; i < n; ++i) {
            power[i] = power[i - 1] + diff[i];
        }
        
        // Lambda для проверки достижимости target
        auto canAchieve = [&](long long target) -> bool {
            vector<long long> addDiff(n + 1, 0);
            long long currAdd = 0;
            long long used = 0;
            
            for (int i = 0; i < n; ++i) {
                currAdd += addDiff[i];
                long long total = power[i] + currAdd;
                if (total < target) {
                    long long need = target - total;
                    used += need;
                    if (used > k) return false;
                    
                    int j = min(i + r, n - 1);      // ставим как можно правее
                    currAdd += need;
                    int end = j + r + 1;
                    if (end < n) addDiff[end] -= need;
                }
            }
            return true;
        };
        
        long long lo = *min_element(power.begin(), power.end());
        long long hi = *max_element(power.begin(), power.end()) + k;
        long long ans = lo;
        
        while (lo <= hi) {
            long long mid = lo + (hi - lo) / 2;
            if (canAchieve(mid)) {
                ans = mid;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return ans;
    }
};

/* Полезные ссылки:
 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 2. Telegram №1 @quadd4rv1n7
 3. Telegram №2 @dupley_maxim_1999
 4. Rutube канал: https://rutube.ru/channel/4218729/
 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 6. YouTube канал: https://www.youtube.com/@it-coders
 7. ВК группа: https://vk.com/science_geeks
*/