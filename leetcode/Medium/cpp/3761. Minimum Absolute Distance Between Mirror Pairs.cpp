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
#include <string>
#include <climits>

using namespace std;

class Solution {
public:
    /**
     * Находит минимальное расстояние между зеркальными парами в массиве.
     *
     * @param nums Исходный массив целых чисел.
     * @return Минимальная разница индексов |i - j| или -1, если пар нет.
     */
    int minMirrorPairDistance(vector<int>& nums) {
        int minDist = INT_MAX;
        unordered_map<int, int> lastSeen; // Ключ: число (или его перевертыш), Значение: индекс
        
        for (int i = 0; i < nums.size(); ++i) {
            int val = nums[i];
            
            // 1. Проверяем, ждало ли нас это число (как перевертыш предыдущего)
            if (lastSeen.count(val)) {
                int dist = i - lastSeen[val];
                minDist = min(minDist, dist);
            }
            
            // 2. Переворачиваем текущее число и сохраняем его индекс как будущую цель
            string s = to_string(val);
            reverse(s.begin(), s.end());
            int rev = stoi(s); // stoi автоматически убирает ведущие нули
            
            lastSeen[rev] = i; // Обновляем индекс (всегда держим самый правый)
        }
        
        return minDist == INT_MAX ? -1 : minDist;
    }
};