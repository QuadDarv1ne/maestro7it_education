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

// JavaScript
var processQueries = function(c, connections, queries) {
    /*
     * Обрабатывает запросы обслуживания энергосети.
     * Использует Union-Find для группировки станций и min-heap для поиска минимальной онлайн станции.
     * 
     * Сложность по времени: O((c + n + q) * α(c))
     * Сложность по памяти: O(c)
     */
    const parent = Array.from({length: c + 1}, (_, i) => i);
    
    // Функция поиска корня с path compression
    const find = (x) => {
        return parent[x] === x ? x : parent[x] = find(parent[x]);
    };
    
    // Объединение двух компонент
    const unite = (x, y) => {
        parent[find(x)] = find(y);
    };
    
    // Строим граф связей
    for (const [u, v] of connections) {
        unite(u, v);
    }
    
    // Создаем отсортированный массив для каждой компоненты
    const comp = new Map();
    for (let i = 1; i <= c; i++) {
        const root = find(i);
        if (!comp.has(root)) comp.set(root, []);
        comp.get(root).push(i);
    }
    
    for (const stations of comp.values()) {
        stations.sort((a, b) => a - b);
    }
    
    const offline = Array(c + 1).fill(false);
    const result = [];
    
    // Обрабатываем запросы
    for (const [type, x] of queries) {
        if (type === 2) {
            // Запрос типа 2: станция переходит в оффлайн
            offline[x] = true;
        } else {
            // Запрос типа 1: поиск онлайн станции для обслуживания
            if (!offline[x]) {
                result.push(x);
            } else {
                const root = find(x);
                const stations = comp.get(root);
                
                // Lazy deletion: удаляем оффлайн станции из массива
                while (stations.length > 0 && offline[stations[0]]) {
                    stations.shift();
                }
                
                result.push(stations.length === 0 ? -1 : stations[0]);
            }
        }
    }
    
    return result;
};
