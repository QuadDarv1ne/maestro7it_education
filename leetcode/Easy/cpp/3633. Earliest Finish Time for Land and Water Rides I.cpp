/**
 * https://leetcode.com/problems/house-robber-ii/description/
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
#include <climits>

using namespace std;

class Solution {
public:
    int earliestFinishTime(vector<int>& landStartTime, vector<int>& landDuration, 
                           vector<int>& waterStartTime, vector<int>& waterDuration) {
        int n = landStartTime.size();
        int m = waterStartTime.size();
        
        auto prepare_data = [](const vector<int>& starts, const vector<int>& durs) {
            vector<tuple<long long, long long, long long>> data;
            for(size_t i = 0; i < starts.size(); ++i) {
                data.emplace_back(starts[i], (long long)starts[i] + durs[i], durs[i]);
            }
            sort(data.begin(), data.end());
            
            int sz = data.size();
            vector<long long> suffix_min_end(sz, LLONG_MAX);
            vector<long long> prefix_min_dur(sz, LLONG_MAX);
            
            if (sz > 0) {
                suffix_min_end[sz-1] = get<1>(data[sz-1]);
                for(int i = sz-2; i >= 0; --i) suffix_min_end[i] = min(get<1>(data[i]), suffix_min_end[i+1]);
                prefix_min_dur[0] = get<2>(data[0]);
                for(int i = 1; i < sz; ++i) prefix_min_dur[i] = min(get<2>(data[i]), prefix_min_dur[i-1]);
            }
            return make_tuple(data, suffix_min_end, prefix_min_dur);
        };
        
        auto [land_data, land_suffix, land_prefix] = prepare_data(landStartTime, landDuration);
        auto [water_data, water_suffix, water_prefix] = prepare_data(waterStartTime, waterDuration);
        
        auto min_end_after = [](const auto& data, const auto& suffix, long long T) -> long long {
            auto it = lower_bound(data.begin(), data.end(), make_tuple(T, -1LL, -1LL));
            if (it == data.end()) return LLONG_MAX;
            return suffix[distance(data.begin(), it)];
        };
        
        auto min_dur_at_or_before = [](const auto& data, const auto& prefix, long long T) -> long long {
            auto it = upper_bound(data.begin(), data.end(), make_tuple(T, LLONG_MAX, LLONG_MAX));
            if (it == data.begin()) return LLONG_MAX;
            return prefix[distance(data.begin(), it) - 1];
        };
        
        long long ans = LLONG_MAX;
        
        for(auto& l : land_data) {
            long long eL = get<1>(l);
            long long opt1a = min_end_after(water_data, water_suffix, eL);
            long long opt1b_dur = min_dur_at_or_before(water_data, water_prefix, eL);
            long long opt1b = (opt1b_dur == LLONG_MAX) ? LLONG_MAX : eL + opt1b_dur;
            ans = min(ans, min(opt1a, opt1b));
        }
        
        for(auto& w : water_data) {
            long long eW = get<1>(w);
            long long opt2a = min_end_after(land_data, land_suffix, eW);
            long long opt2b_dur = min_dur_at_or_before(land_data, land_prefix, eW);
            long long opt2b = (opt2b_dur == LLONG_MAX) ? LLONG_MAX : eW + opt2b_dur;
            ans = min(ans, min(opt2a, opt2b));
        }
        
        return (int)ans;
    }
};