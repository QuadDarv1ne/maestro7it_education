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

public class Solution {
    /// <summary>
    /// Находит максимальное количество мороженого, которое можно купить.
    /// 
    /// Использует жадный подход: сортирует цены по возрастанию и покупает
    /// самое дешевое мороженое, пока хватает монет.
    /// </summary>
    /// <param name="costs">Массив цен на различные виды мороженого</param>
    /// <param name="coins">Количество доступных монет (бюджет)</param>
    /// <returns>Максимальное количество видов мороженого, которое можно купить</returns>
    /// <example>
    /// MaxIceCream([1,3,2,4,1], 7) => 4
    /// MaxIceCream([10,6,8,7,7,8], 5) => 0
    /// MaxIceCream([1,6,3,1,2,5], 20) => 6
    /// </example>
    public int MaxIceCream(int[] costs, int coins) {
        // Сортируем цены по возрастанию для жадного выбора
        Array.Sort(costs);
        
        int count = 0;
        int totalCost = 0;
        
        // Покупаем мороженое, пока хватает монет
        foreach (int cost in costs) {
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

// Альтернативное решение с LINQ (менее эффективное, но элегантное)
public class SolutionLinq {
    /// <summary>
    /// Решение с использованием LINQ для подсчета.
    /// </summary>
    /// <param name="costs">Массив цен на мороженое</param>
    /// <param name="coins">Доступный бюджет</param>
    /// <returns>Количество купленного мороженого</returns>
    public int MaxIceCream(int[] costs, int coins) {
        Array.Sort(costs);
        
        int spent = 0;
        return costs.TakeWhile(cost => {
            spent += cost;
            return spent <= coins;
        }).Count();
    }
}