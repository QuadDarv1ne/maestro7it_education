#include <vector>
#include <algorithm>
#include <numeric>
using namespace std;

class Solution {
public:
    long long maximumHappinessSum(vector<int>& happiness, int k) {
        /**
         * Вычисляет максимальную сумму счастья выбранных детей.
         * 
         * Args:
         *   happiness: вектор значений счастья
         *   k: количество детей для выбора
         * 
         * Returns:
         *   Максимальная сумма счастья
         * 
         * Автор: Дуплей Максим Игоревич
         * ORCID: https://orcid.org/0009-0007-7605-539X
         * GitHub: https://github.com/QuadDarv1ne/
         */
        
        // Сортируем по убыванию
        sort(happiness.rbegin(), happiness.rend());
        
        // Суммируем первые k элементов с учетом уменьшения
        long long total = 0;
        for (int i = 0; i < k; i++) {
            // Текущее счастье после i уменьшений
            long long current = max(0, happiness[i] - i);
            total += current;
        }
        
        return total;
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