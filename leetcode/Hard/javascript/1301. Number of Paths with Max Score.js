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
 * Находит максимальный счет и количество путей с этим счетом.
 * 
 * Игрок начинает с позиции (n-1, n-1) и движется вверх, влево или по диагонали
 * к позиции (0, 0). Цифры на пути добавляются к счету. Символы 'E' и 'S' 
 * не добавляют очков. Препятствия 'X' блокируют путь.
 * 
 * @param {string[]} board - Массив строк, представляющих игровое поле
 * @return {number[]} Массив из двух чисел [max_score, count]:
 *         - max_score: максимально возможный счет, или 0 если пути нет
 *         - count: количество путей с максимальным счетом по модулю 10^9+7
 */
var pathsWithMaxScore = function(board) {
    const MOD = 1000000007;
    const n = board.length;
    
    // dp[i][j] = [max_score, count]
    const dp = Array.from({ length: n }, () => 
        Array.from({ length: n }, () => [-1, 0])
    );
    
    // Начальная позиция
    dp[n-1][n-1] = [0, 1];
    
    // Возможные направления: вниз, вправо, диагональ
    const directions = [[1, 0], [0, 1], [1, 1]];
    
    // Заполняем dp снизу вверх и справа налево
    for (let i = n - 1; i >= 0; i--) {
        for (let j = n - 1; j >= 0; j--) {
            if (board[i][j] === 'X' || (i === n-1 && j === n-1)) {
                continue;
            }
            
            let maxScore = -1;
            let count = 0;
            
            // Проверяем три возможных направления
            for (const [di, dj] of directions) {
                const ni = i + di;
                const nj = j + dj;
                
                if (ni < n && nj < n && dp[ni][nj][0] !== -1) {
                    const score = dp[ni][nj][0];
                    if (score > maxScore) {
                        maxScore = score;
                        count = dp[ni][nj][1];
                    } else if (score === maxScore) {
                        count = (count + dp[ni][nj][1]) % MOD;
                    }
                }
            }
            
            if (maxScore !== -1) {
                // Добавляем очки текущей клетки (если это не 'E' и не 'S')
                if (board[i][j] !== 'E' && board[i][j] !== 'S') {
                    maxScore += parseInt(board[i][j]);
                }
                dp[i][j] = [maxScore, count];
            }
        }
    }
    
    if (dp[0][0][0] === -1) {
        return [0, 0];
    }
    return [dp[0][0][0], dp[0][0][1]];
};