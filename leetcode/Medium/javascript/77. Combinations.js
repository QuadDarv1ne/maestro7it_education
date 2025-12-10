/* ========================== JAVASCRIPT ========================== */

/*
 * LeetCode 77: Combinations
 * https://leetcode.com/problems/combinations/
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
 * 5. YouTube канал: https://www.youtube.com/@it-coders
 * 6. ВК группа: https://vk.com/science_geeks
 */

/**
 * @param {number} n
 * @param {number} k
 * @return {number[][]}
 */
var combine = function(n, k) {
    const result = [];
    
    const backtrack = (start, path) => {
        // Базовый случай: комбинация готова
        if (path.length === k) {
            result.push([...path]); // Копируем массив
            return;
        }
        
        // Оптимизация: останавливаемся раньше
        for (let i = start; i <= n - (k - path.length) + 1; i++) {
            // Выбираем число i
            path.push(i);
            
            // Рекурсивно строим остальную часть
            backtrack(i + 1, path);
            
            // Откатываем выбор (backtracking)
            path.pop();
        }
    };
    
    backtrack(1, []);
    return result;
};