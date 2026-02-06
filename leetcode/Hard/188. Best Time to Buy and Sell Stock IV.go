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

func maxProfit(k int, prices []int) int {
    /**
     * Найти максимальную прибыль от транзакций с акциями при ограничении на количество транзакций.
     * 
     * @param k Максимальное количество разрешенных транзакций
     * @param prices Слайс цен акций по дням
     * @return Максимальная прибыль
     * 
     * Алгоритм:
     * 1. Если k >= n/2, используется алгоритм для неограниченного числа транзакций.
     * 2. Иначе используется динамическое программирование с двумя массивами.
     * 
     * Пример:
     * result := maxProfit(2, []int{3,2,6,5,0,3})
     * // result = 7
     */
    n := len(prices)
    if n <= 1 || k == 0 {
        return 0
    }
    
    // Если k достаточно большое
    if k >= n/2 {
        profit := 0
        for i := 1; i < n; i++ {
            if prices[i] > prices[i-1] {
                profit += prices[i] - prices[i-1]
            }
        }
        return profit
    }
    
    // Динамическое программирование
    buy := make([]int, k+1)
    sell := make([]int, k+1)
    
    // Инициализация buy массива
    for i := 0; i <= k; i++ {
        buy[i] = -1 << 31 // минимальное значение int (аналог -Infinity)
    }
    
    for _, price := range prices {
        for i := k; i >= 1; i-- {
            // Обновляем buy[i] и sell[i]
            if sell[i-1]-price > buy[i] {
                buy[i] = sell[i-1] - price
            }
            if buy[i]+price > sell[i] {
                sell[i] = buy[i] + price
            }
        }
    }
    
    return sell[k]
}