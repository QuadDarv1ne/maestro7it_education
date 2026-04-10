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
#include <climits>

class Solution {
public:
    /**
     * Находит минимальное расстояние между тремя одинаковыми элементами в массиве.
     *
     * Расстояние для тройки индексов (i, j, k) упрощается до 2 * (k - i) при i < j < k.
     * Функция группирует индексы по значениям и перебирает все возможные тройки
     * для каждого числа, чтобы найти минимальную разницу (k - i).
     *
     * @param nums Входной вектор целых чисел.
     * @return Минимальное расстояние или -1, если таких троек нет.
     */
    int minimumDistance(std::vector<int>& nums) {
        std::unordered_map<int, std::vector<int>> positions;
        
        // Группировка индексов
        for (int i = 0; i < nums.size(); ++i) {
            positions[nums[i]].push_back(i);
        }

        int minDist = INT_MAX;

        // Перебор всех значений
        for (const auto& pair : positions) {
            const auto& idxList = pair.second;
            int n = idxList.size();
            
            if (n < 3) continue;

            // Перебор троек индексов для данного значения
            for (int i = 0; i < n - 2; ++i) {
                for (int j = i + 1; j < n - 1; ++j) {
                    for (int k = j + 1; k < n; ++k) {
                        int dist = 2 * (idxList[k] - idxList[i]);
                        if (dist < minDist) {
                            minDist = dist;
                        }
                    }
                }
            }
        }

        return (minDist == INT_MAX) ? -1 : minDist;
    }
};