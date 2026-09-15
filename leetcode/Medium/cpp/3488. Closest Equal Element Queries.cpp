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
#include <unordered_map>
#include <algorithm>

using namespace std;

class Solution {
public:
    /**
     * Находит минимальное кольцевое расстояние до ДРУГОГО равного элемента.
     */
    vector<int> solveQueries(vector<int>& nums, vector<int>& queries) {
        int n = nums.size();
        unordered_map<int, vector<int>> indexMap;
        
        for (int i = 0; i < n; ++i) {
            indexMap[nums[i]].push_back(i);
        }
        
        vector<int> answer;
        answer.reserve(queries.size());
        
        for (int q : queries) {
            int val = nums[q];
            const vector<int>& pos = indexMap[val];
            int m = pos.size();
            
            if (m == 1) {
                answer.push_back(-1);
                continue;
            }
            
            // Бинарный поиск индекса q в pos
            int idx = lower_bound(pos.begin(), pos.end(), q) - pos.begin();
            
            // Берем соседей
            int leftIdx = (idx - 1 + m) % m;
            int rightIdx = (idx + 1) % m;
            
            int leftPos = pos[leftIdx];
            int rightPos = pos[rightIdx];
            
            // Кольцевые расстояния
            int dLeft = abs(q - leftPos);
            int distLeft = min(dLeft, n - dLeft);
            
            int dRight = abs(q - rightPos);
            int distRight = min(dRight, n - dRight);
            
            answer.push_back(min(distLeft, distRight));
        }
        
        return answer;
    }
};