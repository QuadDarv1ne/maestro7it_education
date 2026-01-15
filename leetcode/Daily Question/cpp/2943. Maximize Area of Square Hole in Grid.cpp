/**
 * Максимальная площадь квадратного отверстия в сетке
 * 
 * @param n Количество горизонтальных интервалов
 * @param m Количество вертикальных интервалов
 * @param hBars Горизонтальные удаленные перемычки
 * @param vBars Вертикальные удаленные перемычки
 * @return Максимальная площадь квадратного отверстия
 * 
 * Сложность: O(h log h + v log v) время, O(1) дополнительная память
 * 
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
    int maximizeSquareHoleArea(int n, int m, vector<int>& hBars, vector<int>& vBars) {
        // Сортируем массивы
        sort(hBars.begin(), hBars.end());
        sort(vBars.begin(), vBars.end());
        
        // Находим максимальный непрерывный промежуток в горизонталях
        int maxHGap = 1;
        int current = 1;
        for (int i = 1; i < hBars.size(); i++) {
            if (hBars[i] == hBars[i-1] + 1) {
                current++;
            } else {
                maxHGap = max(maxHGap, current);
                current = 1;
            }
        }
        maxHGap = max(maxHGap, current);
        
        // Находим максимальный непрерывный промежуток в вертикалях
        int maxVGap = 1;
        current = 1;
        for (int i = 1; i < vBars.size(); i++) {
            if (vBars[i] == vBars[i-1] + 1) {
                current++;
            } else {
                maxVGap = max(maxVGap, current);
                current = 1;
            }
        }
        maxVGap = max(maxVGap, current);
        
        // Добавляем 1, так как k промежутков дают отверстие размера k+1
        int side = min(maxHGap, maxVGap) + 1;
        return side * side;
    }
};