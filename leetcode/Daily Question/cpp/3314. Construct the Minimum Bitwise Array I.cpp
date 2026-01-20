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

// ==================== C++ ====================
#include <vector>
using namespace std;

class Solution {
public:
    /**
     * Конструирует минимальный побитовый массив.
     * 
     * Для каждого элемента nums[i] находит минимальное ans[i] такое, что:
     * ans[i] OR (ans[i] + 1) == nums[i]
     * 
     * @param nums вектор простых чисел
     * @return вектор целых чисел, где ans[i] - минимальное значение,
     *         удовлетворяющее условию, или -1 если невозможно
     */
    vector<int> minBitwiseArray(vector<int>& nums) {
        vector<int> ans;
        
        for (int x : nums) {
            // Если x равно 2, решение невозможно
            if (x == 2) {
                ans.push_back(-1);
            } else {
                // Находим первый 0-бит справа (после завершающих единиц)
                for (int i = 1; i < 32; i++) {
                    // Проверяем, является ли бит на позиции i нулем
                    if (((x >> i) & 1) == 0) {
                        // Переворачиваем бит на позиции i-1
                        int result = x ^ (1 << (i - 1));
                        ans.push_back(result);
                        break;
                    }
                }
            }
        }
        
        return ans;
    }
};