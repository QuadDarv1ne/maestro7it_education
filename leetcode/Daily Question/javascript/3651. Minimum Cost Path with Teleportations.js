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
 * Находит минимальную стоимость пути от (0,0) до (m-1,n-1) с возможностью телепортации.
 * 
 * @param {number[][]} grid - Сетка m×n с целыми числами
 * @param {number} k - Максимальное количество телепортаций
 * @return {number} Минимальная стоимость пути
 */
var minCost = function(grid, k) {
    const m = grid.length, n = grid[0].length;
    const INF = 1e9;
    
    // f[t][i][j] = минимальная стоимость достижения (i,j) используя ровно t телепортаций
    const f = Array(k + 1).fill(null).map(() => 
        Array(m).fill(null).map(() => Array(n).fill(INF))
    );
    
    // Базовый случай: телепортации не используются
    f[0][0][0] = 0;
    
    // Заполняем таблицу DP для 0 телепортаций (только обычные ходы)
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (i > 0) {
                f[0][i][j] = Math.min(f[0][i][j], f[0][i-1][j] + grid[i][j]);
            }
            if (j > 0) {
                f[0][i][j] = Math.min(f[0][i][j], f[0][i][j-1] + grid[i][j]);
            }
        }
    }
    
    // Группируем клетки по их значениям для эффективной телепортации
    const valueToCells = new Map();
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (!valueToCells.has(grid[i][j])) {
                valueToCells.set(grid[i][j], []);
            }
            valueToCells.get(grid[i][j]).push([i, j]);
        }
    }
    
    // Сортируем значения по убыванию
    const sortedValues = Array.from(valueToCells.keys()).sort((a, b) => b - a);
    
    // Для каждого количества телепортаций
    for (let t = 1; t <= k; t++) {
        let minCost = INF;
        
        // Обрабатываем клетки в порядке убывания значений
        // Это гарантирует, что когда мы телепортируемся В клетку со значением v,
        // мы уже вычислили стоимости для всех клеток со значением >= v
        for (const val of sortedValues) {
            const cells = valueToCells.get(val);
            
            // Обновляем minCost клетками с текущим значением
            // Это потенциальные источники для телепортации
            for (const [i, j] of cells) {
                minCost = Math.min(minCost, f[t-1][i][j]);
            }
            
            // Все клетки с этим значением можно достичь телепортацией
            // из любой клетки со значением >= этого значения используя t телепортаций
            for (const [i, j] of cells) {
                f[t][i][j] = minCost;
            }
        }
        
        // После телепортации можем делать обычные ходы
        for (let i = 0; i < m; i++) {
            for (let j = 0; j < n; j++) {
                if (i > 0) {
                    f[t][i][j] = Math.min(f[t][i][j], f[t][i-1][j] + grid[i][j]);
                }
                if (j > 0) {
                    f[t][i][j] = Math.min(f[t][i][j], f[t][i][j-1] + grid[i][j]);
                }
            }
        }
    }
    
    // Возвращаем минимальную стоимость используя любое количество телепортаций (от 0 до k)
    let result = INF;
    for (let t = 0; t <= k; t++) {
        result = Math.min(result, f[t][m-1][n-1]);
    }
    return result;
};