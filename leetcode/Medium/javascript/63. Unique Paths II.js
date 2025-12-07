/**
 * @param {number[][]} obstacleGrid
 * @return {number}
 */
var uniquePathsWithObstacles = function(obstacleGrid) {
    /**
     * Автор: Дуплей Максим Игоревич
     * ORCID: https://orcid.org/0009-0007-7605-539X
     * GitHub: https://github.com/QuadDarv1ne/
     * 
     * Задача: Unique Paths II (LeetCode)
     * Алгоритм: Динамическое программирование для подсчета путей с препятствиями
     * Сложность: O(m * n) по времени, O(m * n) по памяти
     * 
     * Идея решения:
     * 1. Создаем DP таблицу для хранения количества путей к каждой клетке
     * 2. Если клетка содержит препятствие - путей к ней 0
     * 3. Иначе: количество путей = пути сверху + пути слева
     * 4. dp[i][j] = dp[i-1][j] + dp[i][j-1]
     */
    
    // Если старт или финиш заблокированы
    if (obstacleGrid[0][0] === 1) {
        return 0;
    }
    
    const m = obstacleGrid.length;
    const n = obstacleGrid[0].length;
    
    // Создаем DP таблицу
    const dp = Array.from({ length: m }, () => Array(n).fill(0));
    dp[0][0] = 1; // Стартовая позиция
    
    // Заполняем DP таблицу
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            // Пропускаем стартовую позицию
            if (i === 0 && j === 0) {
                continue;
            }
            
            // Если текущая клетка - препятствие
            if (obstacleGrid[i][j] === 1) {
                dp[i][j] = 0;
            } else {
                // Суммируем пути сверху и слева
                const fromTop = (i > 0) ? dp[i-1][j] : 0;
                const fromLeft = (j > 0) ? dp[i][j-1] : 0;
                dp[i][j] = fromTop + fromLeft;
            }
        }
    }
    
    return dp[m-1][n-1];
};

/*
 * Полезные ссылки автора:
 * Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * Telegram: @quadd4rv1n7, @dupley_maxim_1999
 * Rutube: https://rutube.ru/channel/4218729/
 * Plvideo: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * YouTube: https://www.youtube.com/@it-coders
 * VK: https://vk.com/science_geeks
 */