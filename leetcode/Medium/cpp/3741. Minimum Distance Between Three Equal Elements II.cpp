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

using namespace std;

/**
 * @brief Находит минимальное расстояние между тремя равными элементами в массиве.
 *
 * Алгоритм группирует индексы каждого уникального числа, а затем для каждой
 * группы из >=3 элементов вычисляет расстояние между первым и третьим индексом
 * в каждой тройке последовательных индексов. Минимальное из этих значений
 * возвращается как результат.
 *
 * @param nums Входной массив целых чисел.
 * @return Минимальное расстояние или -1, если таких троек нет.
 */
class Solution {
public:
    int minimumDistance(vector<int>& nums) {
        // Группируем индексы по значениям
        unordered_map<int, vector<int>> valueToIndices;
        for (int i = 0; i < nums.size(); ++i) {
            valueToIndices[nums[i]].push_back(i);
        }

        int minDist = INT_MAX;
        for (const auto& pair : valueToIndices) {
            const auto& indices = pair.second;
            int m = indices.size();
            if (m >= 3) {
                // Рассматриваем все тройки последовательных индексов
                for (int i = 0; i <= m - 3; ++i) {
                    // Расстояние между тремя равными элементами вычисляется как 2*(z - x)
                    int dist = 2 * (indices[i + 2] - indices[i]);
                    minDist = min(minDist, dist);
                }
            }
        }
        return minDist == INT_MAX ? -1 : minDist;
    }
};