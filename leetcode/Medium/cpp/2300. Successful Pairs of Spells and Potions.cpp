/*
https://leetcode.com/problems/successful-pairs-of-spells-and-potions/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<int> successfulPairs(vector<int>& spells, vector<int>& potions, long long success) {
        sort(potions.begin(), potions.end());
        int m = potions.size();
        vector<int> ans;
        ans.reserve(spells.size());
        for (int spell : spells) {
            // если spell == 0, то его продукты нули, не будут >= success (если success > 0)
            // но по условию spells[i], potions[j] ≥ 1, так что, скорее всего, это не нужно
            long long req = (success + spell - 1) / spell;  // минимальное значение зелья
            // бинарный поиск первого элемента >= req
            auto it = lower_bound(potions.begin(), potions.end(), req);
            int idx = it - potions.begin();
            ans.push_back(m - idx);
        }
        return ans;
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