"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

import bisect

class Solution:
    def earliestFinishTime(self, landStartTime, landDuration, waterStartTime, waterDuration):
        if not landStartTime or not waterStartTime:
            return -1
            
        def prepare_data(startTimes, durations):
            data = [(s, s + d, d) for s, d in zip(startTimes, durations)]
            data.sort(key=lambda x: x[0])
            
            n = len(data)
            suffix_min_end = [float('inf')] * n
            prefix_min_dur = [float('inf')] * n
            
            if n > 0:
                suffix_min_end[-1] = data[-1][1]
                for i in range(n - 2, -1, -1):
                    suffix_min_end[i] = min(data[i][1], suffix_min_end[i + 1])
                    
                prefix_min_dur[0] = data[0][2]
                for i in range(1, n):
                    prefix_min_dur[i] = min(data[i][2], prefix_min_dur[i - 1])
                    
            return data, suffix_min_end, prefix_min_dur
            
        def min_end_after(data, suffix_min, T):
            idx = bisect.bisect_left(data, (T, -1, -1))
            return suffix_min[idx] if idx < len(data) else float('inf')
            
        def min_dur_at_or_before(data, prefix_min, T):
            idx = bisect.bisect_right(data, (T, float('inf'), float('inf'))) - 1
            return prefix_min[idx] if idx >= 0 else float('inf')
            
        land_data, land_suffix, land_prefix = prepare_data(landStartTime, landDuration)
        water_data, water_suffix, water_prefix = prepare_data(waterStartTime, waterDuration)
        
        ans = float('inf')
        
        # Вариант 1: Сначала суша, потом вода
        for s_l, e_l, d_l in land_data:
            opt1a = min_end_after(water_data, water_suffix, e_l)
            opt1b_dur = min_dur_at_or_before(water_data, water_prefix, e_l)
            opt1b = e_l + opt1b_dur if opt1b_dur != float('inf') else float('inf')
            ans = min(ans, opt1a, opt1b)
            
        # Вариант 2: Сначала вода, потом суша
        for s_w, e_w, d_w in water_data:
            opt2a = min_end_after(land_data, land_suffix, e_w)
            opt2b_dur = min_dur_at_or_before(land_data, land_prefix, e_w)
            opt2b = e_w + opt2b_dur if opt2b_dur != float('inf') else float('inf')
            ans = min(ans, opt2a, opt2b)
            
        return int(ans) if ans != float('inf') else -1