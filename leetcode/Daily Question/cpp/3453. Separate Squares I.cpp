/**
 * Разделение квадратов горизонтальной линией
 * 
 * @param squares Массив квадратов [x, y, длина]
 * @return Минимальная y-координата разделяющей линии
 * 
 * Сложность: Время O(n log max_y), Память O(1)
 *
 * Автор: Дуплей Максим Игоревич
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
    double separateSquares(vector<vector<int>>& squares) {
        // Вычисление общей площади всех квадратов
        long long totalArea = 0;
        double maxY = 0.0;
        
        for (const auto& sq : squares) {
            long long l = sq[2];
            totalArea += l * l;
            maxY = max(maxY, (double)(sq[1] + sq[2]));
        }
        
        double targetArea = totalArea / 2.0;
        double low = 0.0;
        double high = maxY;
        
        // Функция для вычисления площади ниже линии y
        auto areaBelow = [&](double yLine) {
            double area = 0.0;
            for (const auto& sq : squares) {
                int y = sq[1];
                int l = sq[2];
                
                if (y >= yLine) {
                    // Квадрат полностью выше линии
                    continue;
                } else if (y + l <= yLine) {
                    // Квадрат полностью ниже линии
                    area += (double)l * l;
                } else {
                    // Квадрат пересекает линию
                    double height = yLine - y;
                    area += height * l;
                }
            }
            return area;
        };
        
        // Бинарный поиск с фиксированным числом итераций для точности
        for (int i = 0; i < 100; i++) {
            double mid = (low + high) / 2.0;
            if (areaBelow(mid) < targetArea) {
                low = mid;
            } else {
                high = mid;
            }
        }
        
        return low;
    }
};