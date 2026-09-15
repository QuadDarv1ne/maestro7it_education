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

import java.util.Arrays;

class Solution {
    /**
     * Находит максимальное количество мороженого, которое можно купить.
     * 
     * Использует жадный подход: сортирует цены по возрастанию и покупает
     * самое дешевое мороженое, пока хватает монет.
     *
     * @param costs массив цен на различные виды мороженого
     * @param coins количество доступных монет (бюджет)
     * @return максимальное количество видов мороженого, которое можно купить
     *
     * Пример:
     * maxIceCream([1,3,2,4,1], 7) -> 4
     * maxIceCream([10,6,8,7,7,8], 5) -> 0
     * maxIceCream([1,6,3,1,2,5], 20) -> 6
     */
    public int maxIceCream(int[] costs, int coins) {
        // Сортируем цены по возрастанию для жадного выбора
        Arrays.sort(costs);
        
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
}

// Альтернативное решение с использованием Stream API
class SolutionStream {
    /**
     * Решение с использованием Stream API для функционального подхода.
     *
     * @param costs массив цен на мороженое
     * @param coins доступный бюджет
     * @return количество купленного мороженого
     */
    public int maxIceCream(int[] costs, int coins) {
        Arrays.sort(costs);
        
        // Используем изменяемый счетчик для отслеживания потраченных монет
        final int[] spent = {0};
        
        return (int) Arrays.stream(costs)
            .takeWhile(cost -> {
                spent[0] += cost;
                return spent[0] <= coins;
            })
            .count();
    }
}