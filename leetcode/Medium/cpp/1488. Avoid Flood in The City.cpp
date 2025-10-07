/*
https://leetcode.com/problems/avoid-flood-in-the-city/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

#include <vector>
#include <unordered_map>
#include <set>
using namespace std;

class Solution {
public:
    vector<int> avoidFlood(vector<int>& rains) {
        /*
        Идея:
        - lastRain[lake] хранит последний индекс дождя над озером.
        - dryDays хранит индексы сухих дней (set для поиска первого > lastRain[lake]).
        - Когда дождь над озером уже полным, ищем сухой день для осушения.
        */
        unordered_map<int,int> lastRain;
        set<int> dryDays;
        vector<int> res(rains.size(), -1);

        for (int i = 0; i < rains.size(); i++) {
            int lake = rains[i];
            if (lake == 0) {
                dryDays.insert(i);
                res[i] = 1;
            } else {
                if (lastRain.count(lake)) {
                    auto it = dryDays.upper_bound(lastRain[lake]);
                    if (it == dryDays.end()) return {};
                    res[*it] = lake;
                    dryDays.erase(it);
                }
                lastRain[lake] = i;
                res[i] = -1;
            }
        }
        return res;
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