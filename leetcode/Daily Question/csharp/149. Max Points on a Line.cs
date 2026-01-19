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
    public int MaxPoints(int[][] points) {
        int n = points.Length;
        if (n <= 2) return n;
        
        int maxPoints = 1;
        
        for (int i = 0; i < n; i++) {
            // Используем Dictionary для подсчета точек с одинаковым наклоном
            Dictionary<string, int> slopeCount = new Dictionary<string, int>();
            int duplicates = 1; // Начинаем с 1 (сама точка)
            int currentMax = 0;
            
            for (int j = i + 1; j < n; j++) {
                int dx = points[j][0] - points[i][0];
                int dy = points[j][1] - points[i][1];
                
                // Проверка на дубликаты
                if (dx == 0 && dy == 0) {
                    duplicates++;
                    continue;
                }
                
                // Вычисление НОД для нормализации дроби
                int g = Gcd(dx, dy);
                dx /= g;
                dy /= g;
                
                // Нормализация знаков для устранения дублирования
                // Например, (1, -1) и (-1, 1) должны быть одинаковыми
                if (dx < 0 || (dx == 0 && dy < 0)) {
                    dx = -dx;
                    dy = -dy;
                }
                
                // Создаем ключ для наклона
                string key = dx + "_" + dy;
                if (!slopeCount.ContainsKey(key)) {
                    slopeCount[key] = 0;
                }
                slopeCount[key]++;
                currentMax = Math.Max(currentMax, slopeCount[key]);
            }
            
            // Обновляем максимальное количество точек
            maxPoints = Math.Max(maxPoints, currentMax + duplicates);
        }
        
        return maxPoints;
    }
    
    // Функция для вычисления НОД
    private int Gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return Math.Abs(a);
    }
}