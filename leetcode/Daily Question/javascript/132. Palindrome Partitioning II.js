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
 * @param {string} s
 * @return {number}
 */
var minCut = function(s) {
    /**
     * Находит минимальное количество разрезов для разбиения строки на палиндромы.
     * 
     * Алгоритм:
     * 1. Создаем матрицу для проверки палиндромов
     * 2. Используем динамическое программирование для нахождения минимальных разрезов
     * 
     * Сложность: O(n²) время, O(n²) память
     */
    
    const n = s.length;
    if (n <= 1) return 0;
    
    // 1. Матрица для проверки палиндромов
    const isPalindrome = Array.from({length: n}, () => new Array(n).fill(false));
    
    // Все подстроки длины 1 - палиндромы
    for (let i = 0; i < n; i++) {
        isPalindrome[i][i] = true;
    }
    
    // Проверяем подстроки длины 2 и больше
    for (let length = 2; length <= n; length++) {
        for (let i = 0; i <= n - length; i++) {
            const j = i + length - 1;
            
            if (length === 2) {
                isPalindrome[i][j] = (s[i] === s[j]);
            } else {
                isPalindrome[i][j] = (s[i] === s[j] && isPalindrome[i + 1][j - 1]);
            }
        }
    }
    
    // 2. Динамическое программирование для минимальных разрезов
    const minCuts = new Array(n + 1).fill(Infinity);
    minCuts[0] = -1; // Для пустой строки
    
    for (let i = 1; i <= n; i++) {
        for (let j = 0; j < i; j++) {
            // Если s.substring(j, i) - палиндром
            if (isPalindrome[j][i - 1]) {
                minCuts[i] = Math.min(minCuts[i], minCuts[j] + 1);
            }
        }
    }
    
    return minCuts[n];
};