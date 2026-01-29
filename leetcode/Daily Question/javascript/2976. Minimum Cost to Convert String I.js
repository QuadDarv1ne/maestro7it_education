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

var minimumCost = function(source, target, original, changed, cost) {
    const INF = Number.MAX_SAFE_INTEGER;
    // Матрица 26x26 для минимальных стоимостей преобразований
    const dist = Array.from({ length: 26 }, () => new Array(26).fill(INF));
    
    // Инициализация: преобразование символа в себя стоит 0
    for (let i = 0; i < 26; i++) {
        dist[i][i] = 0;
    }
    
    // Добавляем заданные преобразования
    for (let i = 0; i < original.length; i++) {
        const u = original[i].charCodeAt(0) - 97; // Извлекаем первый символ строки
        const v = changed[i].charCodeAt(0) - 97;
        dist[u][v] = Math.min(dist[u][v], cost[i]);
    }
    
    // Алгоритм Флойда-Уоршелла
    for (let k = 0; k < 26; k++) {
        for (let i = 0; i < 26; i++) {
            if (dist[i][k] === INF) continue;
            for (let j = 0; j < 26; j++) {
                if (dist[k][j] === INF) continue;
                dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
            }
        }
    }
    
    // Вычисляем общую стоимость
    let total = 0;
    for (let i = 0; i < source.length; i++) {
        const u = source.charCodeAt(i) - 97;
        const v = target.charCodeAt(i) - 97;
        
        if (dist[u][v] === INF) {
            return -1;
        }
        total += dist[u][v];
    }
    
    return total;
};