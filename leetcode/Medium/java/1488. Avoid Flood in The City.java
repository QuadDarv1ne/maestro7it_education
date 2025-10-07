/*
https://leetcode.com/problems/avoid-flood-in-the-city/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

import java.util.*;

class Solution {
    public int[] avoidFlood(int[] rains) {
        /*
        Идея:
        - lastRain хранит последний день дождя над озером.
        - dryDays (TreeSet) хранит индексы сухих дней.
        - При дожде над уже полным озером ищем ближайший сухой день для осушения.
        */
        Map<Integer, Integer> lastRain = new HashMap<>();
        TreeSet<Integer> dryDays = new TreeSet<>();
        int[] res = new int[rains.length];
        Arrays.fill(res, -1);

        for (int i = 0; i < rains.length; i++) {
            int lake = rains[i];
            if (lake == 0) {
                dryDays.add(i);
                res[i] = 1;
            } else {
                if (lastRain.containsKey(lake)) {
                    Integer dryIdx = dryDays.higher(lastRain.get(lake));
                    if (dryIdx == null) return new int[0];
                    res[dryIdx] = lake;
                    dryDays.remove(dryIdx);
                }
                lastRain.put(lake, i);
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