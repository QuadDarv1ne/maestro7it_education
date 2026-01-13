/**
 * Разделение квадратов горизонтальной линией
 * 
 * @param {number[][]} squares Массив квадратов [x, y, длина]
 * @return {number} Минимальная y-координата разделяющей линии
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

/**
 * @param {number[][]} squares
 * @return {number}
 */
var separateSquares = function(squares) {
    // Вычисление общей площади всех квадратов
    let totalArea = 0;
    let maxY = 0;
    
    for (const [x, y, l] of squares) {
        totalArea += l * l;
        maxY = Math.max(maxY, y + l);
    }
    
    const targetArea = totalArea / 2.0;
    let low = 0.0;
    let high = maxY;
    
    // Функция для вычисления площади ниже линии y
    const areaBelow = (yLine) => {
        let area = 0.0;
        for (const [x, y, l] of squares) {
            if (y >= yLine) {
                // Квадрат полностью выше линии
                continue;
            } else if (y + l <= yLine) {
                // Квадрат полностью ниже линии
                area += l * l;
            } else {
                // Квадрат пересекает линию
                const height = yLine - y;
                area += height * l;
            }
        }
        return area;
    };
    
    // Бинарный поиск с фиксированным числом итераций для точности
    for (let i = 0; i < 100; i++) {
        const mid = (low + high) / 2.0;
        if (areaBelow(mid) < targetArea) {
            low = mid;
        } else {
            high = mid;
        }
    }
    
    return low;
};