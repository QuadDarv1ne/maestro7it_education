/**
 * https://leetcode.com/problems/contains-duplicate-iii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "220. Contains Duplicate III"
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
#include <set>
#include <cmath>

using namespace std;

class Solution {
public:
    bool containsNearbyAlmostDuplicate(vector<int>& nums, int k, int t) {
        if (k < 0 || t < 0) return false;
        
        set<long> window;
        
        for (int i = 0; i < nums.size(); i++) {
            long num = nums[i];
            
            // Находим наименьший элемент ≥ num - t
            auto it = window.lower_bound(num - (long)t);
            
            // Проверяем, удовлетворяет ли условию
            if (it != window.end() && *it <= num + (long)t) {
                return true;
            }
            
            // Добавляем текущий элемент
            window.insert(num);
            
            // Удаляем элемент, который выходит за пределы окна
            if (i >= k) {
                window.erase((long)nums[i - k]);
            }
        }
        
        return false;
    }
};