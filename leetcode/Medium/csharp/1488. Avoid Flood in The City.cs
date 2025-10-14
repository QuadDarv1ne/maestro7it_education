/*
https://leetcode.com/problems/avoid-flood-in-the-city/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

using System;
using System.Collections.Generic;

public class Solution {
    public int[] AvoidFlood(int[] rains) {
        var lastRain = new Dictionary<int,int>();
        var dryDays = new SortedDictionary<int,int>();
        int n = rains.Length;
        int[] res = new int[n];
        for(int i=0;i<n;i++) res[i] = -1;

        for(int i=0;i<n;i++){
            int lake = rains[i];
            if(lake == 0){
                dryDays[i] = 1; // по умолчанию
                res[i] = 1;
            } else {
                if(lastRain.ContainsKey(lake)){
                    int prevDay = lastRain[lake];
                    // ищем первый сухой день > prevDay
                    int dryIdx = -1;
                    foreach(var key in dryDays.Keys){
                        if(key > prevDay){
                            dryIdx = key;
                            break;
                        }
                    }
                    if(dryIdx == -1) return new int[0]; // наводнение
                    res[dryIdx] = lake;
                    dryDays.Remove(dryIdx);
                }
                lastRain[lake] = i;
                res[i] = -1;
            }
        }
        return res;
    }
}

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