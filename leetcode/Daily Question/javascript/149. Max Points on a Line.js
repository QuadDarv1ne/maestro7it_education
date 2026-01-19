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

/**
 * @param {number[][]} points
 * @return {number}
 */
var maxPoints = function(points) {
    const n = points.length;
    if (n <= 2) return n;
    
    let maxPoints = 1;
    
    for (let i = 0; i < n; i++) {
        // Используем Map для подсчета точек с одинаковым наклоном
        const slopeCount = new Map();
        let duplicates = 1; // Начинаем с 1 (сама точка)
        let currentMax = 0;
        
        for (let j = i + 1; j < n; j++) {
            let dx = points[j][0] - points[i][0];
            let dy = points[j][1] - points[i][1];
            
            // Проверка на дубликаты
            if (dx === 0 && dy === 0) {
                duplicates++;
                continue;
            }
            
            // Вычисление НОД для нормализации дроби
            const g = gcd(dx, dy);
            dx /= g;
            dy /= g;
            
            // Нормализация знаков для устранения дублирования
            // Например, (1, -1) и (-1, 1) должны быть одинаковыми
            if (dx < 0 || (dx === 0 && dy < 0)) {
                dx = -dx;
                dy = -dy;
            }
            
            // Создаем ключ для наклона
            const key = `${dx}_${dy}`;
            const count = (slopeCount.get(key) || 0) + 1;
            slopeCount.set(key, count);
            currentMax = Math.max(currentMax, count);
        }
        
        // Обновляем максимальное количество точек
        maxPoints = Math.max(maxPoints, currentMax + duplicates);
    }
    
    return maxPoints;
};

// Функция для вычисления НОД
function gcd(a, b) {
    while (b !== 0) {
        const temp = b;
        b = a % b;
        a = temp;
    }
    return Math.abs(a);
}