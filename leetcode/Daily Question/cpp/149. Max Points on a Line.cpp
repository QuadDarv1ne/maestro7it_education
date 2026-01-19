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

class Solution {
public:
    int maxPoints(vector<vector<int>>& points) {
        int n = points.size();
        if (n <= 2) return n;
        
        int maxPoints = 0;
        
        for (int i = 0; i < n; i++) {
            // Используем unordered_map для подсчета точек с одинаковым наклоном
            unordered_map<string, int> slopeCount;
            int duplicates = 0; // Количество точек, совпадающих с текущей
            int currentMax = 0; // Максимум для текущей точки
            
            for (int j = 0; j < n; j++) {
                if (i == j) continue;
                
                int dx = points[j][0] - points[i][0];
                int dy = points[j][1] - points[i][1];
                
                // Проверка на дубликаты
                if (dx == 0 && dy == 0) {
                    duplicates++;
                    continue;
                }
                
                // Вычисление НОД для нормализации дроби
                int g = gcd(dx, dy);
                dx /= g;
                dy /= g;
                
                // Нормализация знаков для устранения дублирования
                // Например, (1, -1) и (-1, 1) должны быть одинаковыми
                if (dx < 0 || (dx == 0 && dy < 0)) {
                    dx = -dx;
                    dy = -dy;
                }
                
                // Создаем ключ для наклона
                string key = to_string(dx) + "_" + to_string(dy);
                slopeCount[key]++;
                currentMax = max(currentMax, slopeCount[key]);
            }
            
            // Обновляем максимальное количество точек
            // +1 для текущей точки
            maxPoints = max(maxPoints, currentMax + duplicates + 1);
            
            // Если точек много, можем раньше завершить
            if (maxPoints >= n - i) break;
        }
        
        return maxPoints;
    }
    
private:
    // Функция для вычисления НОД
    int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return abs(a);
    }
};