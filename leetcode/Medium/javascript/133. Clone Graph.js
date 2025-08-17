/**
 * https://leetcode.com/problems/clone-graph/description/
 */

/**
 * Определение узла графа.
 * function Node(val, neighbors) {
 *     this.val = val === undefined ? 0 : val;
 *     this.neighbors = neighbors === undefined ? [] : neighbors;
 * }
 */

/**
 * Клонирует связный неориентированный граф.
 * Используется DFS с Map для отслеживания уже клонированных узлов.
 *
 * @param {Node} node - узел графа
 * @return {Node} глубокая копия графа
 */
var cloneGraph = function(node) {
    if (!node) return null;
    const map = new Map();

    function dfs(n) {
        if (map.has(n.val)) return map.get(n.val);

        const cloneNode = new Node(n.val);
        map.set(n.val, cloneNode);

        for (const neighbor of n.neighbors) {
            cloneNode.neighbors.push(dfs(neighbor));
        }

        return cloneNode;
    }

    return dfs(node);
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/