/**
 * https://leetcode.com/problems/clone-graph/description/
 */

import java.util.*;

/**
 * Определение узла графа.
 */
// class Node {
//     public int val;
//     public List<Node> neighbors;
//     public Node() {
//         val = 0;
//         neighbors = new ArrayList<>();
//     }
//     public Node(int _val) {
//         val = _val;
//         neighbors = new ArrayList<>();
//     }
//     public Node(int _val, List<Node> _neighbors) {
//         val = _val;
//         neighbors = _neighbors;
//     }
// }

class Solution {
    /**
     * Клонирует связный неориентированный граф.
     * Используется DFS с хэш-таблицей для отслеживания уже клонированных узлов.
     * @param node узел графа
     * @return глубокая копия графа
     */
    public Node cloneGraph(Node node) {
        if (node == null) return null;
        Map<Integer, Node> map = new HashMap<>();
        return clone(node, map);
    }

    private Node clone(Node node, Map<Integer, Node> map) {
        if (map.containsKey(node.val)) return map.get(node.val);

        Node cloneNode = new Node(node.val);
        map.put(node.val, cloneNode);

        for (Node neighbor : node.neighbors) {
            cloneNode.neighbors.add(clone(neighbor, map));
        }

        return cloneNode;
    }
}

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