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
    bool containsNearbyDuplicate(vector<int>& nums, int k) {
        // Хеш-таблица для хранения последнего индекса каждого числа
        unordered_map<int, int> indexMap;
        
        for (int i = 0; i < nums.size(); i++) {
            int num = nums[i];
            
            // Проверяем, встречалось ли число раньше
            if (indexMap.find(num) != indexMap.end()) {
                // Проверяем разницу индексов
                if (i - indexMap[num] <= k) {
                    return true;
                }
            }
            
            // Обновляем индекс для текущего числа
            indexMap[num] = i;
        }
        
        return false;
    }
};