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
#include <algorithm>

class Solution {
public:
    /**
     * Находит максимальное количество мороженого, которое можно купить.
     * 
     * Использует жадный подход: сортирует цены по возрастанию и покупает
     * самое дешевое мороженое, пока хватает монет.
     *
     * @param costs вектор цен на различные виды мороженого
     * @param coins количество доступных монет (бюджет)
     * @return int максимальное количество видов мороженого, которое можно купить
     *
     * Пример:
     * maxIceCream([1,3,2,4,1], 7) -> 4
     * maxIceCream([10,6,8,7,7,8], 5) -> 0
     * maxIceCream([1,6,3,1,2,5], 20) -> 6
     */
    int maxIceCream(std::vector<int>& costs, int coins) {
        // Сортируем цены по возрастанию для жадного выбора
        std::sort(costs.begin(), costs.end());
        
        int count = 0;
        int totalCost = 0;
        
        // Покупаем мороженое, пока хватает монет
        for (int cost : costs) {
            if (totalCost + cost <= coins) {
                totalCost += cost;
                count++;
            } else {
                break;
            }
        }
        
        return count;
    }
};

// Альтернативное решение с оптимизацией
class SolutionOpt {
public:
    /**
     * Оптимизированное решение с ранним выходом из цикла.
     *
     * @param costs вектор цен на различные виды мороженого
     * @param coins количество доступных монет
     * @return int максимальное количество видов мороженого
     */
    int maxIceCream(std::vector<int>& costs, int coins) {
        std::sort(costs.begin(), costs.end());
        
        for (int i = 0; i < costs.size(); i++) {
            coins -= costs[i];
            if (coins < 0) {
                return i;
            }
        }
        
        return costs.size();
    }
};
