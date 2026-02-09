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
    /**
     * Вычисляет общую площадь, покрываемую двумя прямоугольниками.
     * 
     * Алгоритм:
     * 1. Вычисляет площади каждого прямоугольника.
     * 2. Находит площадь пересечения прямоугольников (если оно есть).
     * 3. Возвращает сумму площадей минус площадь пересечения.
     * 
     * Формула:
     * Общая площадь = Площадь1 + Площадь2 - ПлощадьПересечения
     * 
     * Сложность:
     * Время: O(1)
     * Пространство: O(1)
     * 
     * @param ax1, ay1, ax2, ay2 Координаты первого прямоугольника
     * @param bx1, by1, bx2, by2 Координаты второго прямоугольника
     * @return Общая площадь, покрываемая двумя прямоугольниками
     * 
     * Пример:
     * Вход: ax1=-3, ay1=0, ax2=3, ay2=4, bx1=0, by1=-1, bx2=9, by2=2
     * Площадь1 = 24, Площадь2 = 27, Пересечение = 6
     * Выход: 24 + 27 - 6 = 45
     */
    public int ComputeArea(int ax1, int ay1, int ax2, int ay2, 
                          int bx1, int by1, int bx2, int by2) {
        // Вычисляем площади каждого прямоугольника
        long areaA = (long)(ax2 - ax1) * (ay2 - ay1);
        long areaB = (long)(bx2 - bx1) * (by2 - by1);
        
        // Находим координаты пересечения
        int overlapWidth = Math.Max(0, Math.Min(ax2, bx2) - Math.Max(ax1, bx1));
        int overlapHeight = Math.Max(0, Math.Min(ay2, by2) - Math.Max(ay1, by1));
        
        // Вычисляем площадь пересечения
        long overlapArea = (long)overlapWidth * overlapHeight;
        
        // Общая площадь
        return (int)(areaA + areaB - overlapArea);
    }
}