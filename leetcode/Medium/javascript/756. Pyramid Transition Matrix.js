/**
 * https://leetcode.com/problems/pyramid-transition-matrix/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Pyramid Transition Matrix"
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
 * Определяет, можно ли построить пирамиду из заданного основания.
 * 
 * @param {string} bottom - строка основания пирамиды
 * @param {string[]} allowed - список разрешенных троек вида "XYZ", где XY - основание, Z - вершина
 * @return {boolean} - true если пирамиду можно построить, иначе false
 */
var pyramidTransition = function(bottom, allowed) {
    // Создаем карту для быстрого поиска разрешенных вершин
    const allowedMap = new Map();
    for (const triple of allowed) {
        const base = triple.slice(0, 2);
        const top = triple[2];
        if (!allowedMap.has(base)) {
            allowedMap.set(base, []);
        }
        allowedMap.get(base).push(top);
    }
    
    // Мемоизация для оптимизации
    const memo = new Map();
    
    /**
     * Рекурсивно строим пирамиду.
     * @param {string} current - текущий уровень пирамиды
     * @return {boolean} - можно ли построить пирамиду от этого уровня
     */
    const dfs = (current) => {
        // Если уже вычисляли для этого уровня - возвращаем результат
        if (memo.has(current)) {
            return memo.get(current);
        }
        
        // Базовый случай: достигли вершины пирамиды
        if (current.length === 1) {
            memo.set(current, true);
            return true;
        }
        
        // Генерируем все возможные следующие уровни
        const nextLevels = [];
        generateNextLevels(current, "", 0, allowedMap, nextLevels);
        
        // Если не удалось сгенерировать следующий уровень
        if (nextLevels.length === 0) {
            memo.set(current, false);
            return false;
        }
        
        // Проверяем каждый возможный следующий уровень
        for (const next of nextLevels) {
            if (dfs(next)) {
                memo.set(current, true);
                return true;
            }
        }
        
        memo.set(current, false);
        return false;
    };
    
    return dfs(bottom);
};

/**
 * Генерирует все возможные следующие уровни пирамиды.
 * @param {string} current - текущий уровень
 * @param {string} next - строящийся следующий уровень
 * @param {number} idx - текущая позиция
 * @param {Map} allowedMap - карта разрешенных переходов
 * @param {string[]} result - массив для результатов
 */
function generateNextLevels(current, next, idx, allowedMap, result) {
    // Если следующий уровень полностью построен
    if (next.length === current.length - 1) {
        result.push(next);
        return;
    }
    
    // Текущая пара символов
    const pair = current.slice(idx, idx + 2);
    
    // Если для этой пары нет разрешенных вершин - прерываем генерацию
    const tops = allowedMap.get(pair);
    if (!tops) {
        return;
    }
    
    // Перебираем все возможные вершины для текущей пары
    for (const top of tops) {
        generateNextLevels(current, next + top, idx + 1, allowedMap, result);
    }
}