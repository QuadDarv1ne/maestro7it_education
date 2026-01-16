public class Solution {
    public int MaxProfit(int[] prices) {
        /**
         * Альтернативный подход: два прохода
         * 1. Слева направо: максимальная прибыль от одной транзакции до i-го дня
         * 2. Справа налево: максимальная прибыль от одной транзакции после i-го дня
         * 3. Суммируем лучшие результаты
         * 
         * Временная сложность: O(n)
         * Пространственная сложность: O(n)
         */
        
        if (prices == null || prices.Length < 2) {
            return 0;
        }
        
        int n = prices.Length;
        
        // Массив для максимальной прибыли от одной транзакции слева до i
        int[] leftProfit = new int[n];
        
        // Массив для максимальной прибыли от одной транзакции справа от i
        int[] rightProfit = new int[n];
        
        // Заполняем leftProfit
        int minPrice = prices[0];
        for (int i = 1; i < n; i++) {
            minPrice = Math.Min(minPrice, prices[i]);
            leftProfit[i] = Math.Max(leftProfit[i - 1], prices[i] - minPrice);
        }
        
        // Заполняем rightProfit
        int maxPrice = prices[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            maxPrice = Math.Max(maxPrice, prices[i]);
            rightProfit[i] = Math.Max(rightProfit[i + 1], maxPrice - prices[i]);
        }
        
        // Находим максимальную сумму двух транзакций
        int maxProfit = 0;
        for (int i = 0; i < n; i++) {
            maxProfit = Math.Max(maxProfit, leftProfit[i] + rightProfit[i]);
        }
        
        return maxProfit;
    }
}