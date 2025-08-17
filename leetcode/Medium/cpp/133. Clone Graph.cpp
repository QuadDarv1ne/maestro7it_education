/**
 * https://leetcode.com/problems/clone-graph/description/
 */

#include <vector>
#include <unordered_map>
using namespace std;

/*
// Определение узла графа.
class Node {
public:
    int val;
    vector<Node*> neighbors;
    Node() : val(0), neighbors(vector<Node*>()) {}
    Node(int _val) : val(_val), neighbors(vector<Node*>()) {}
    Node(int _val, vector<Node*> _neighbors) : val(_val), neighbors(_neighbors) {}
};
*/

class Solution {
public:
    /**
     * Клонирует связный неориентированный граф.
     * Используется DFS с хэш-таблицей для отслеживания уже клонированных узлов.
     * @param node — узел графа
     * @return глубокая копия графа
     */
    Node* cloneGraph(Node* node) {
        if (!node) return nullptr;
        unordered_map<int, Node*> map;
        return clone(node, map);
    }

private:
    Node* clone(Node* node, unordered_map<int, Node*>& map) {
        if (map.count(node->val)) return map[node->val];

        Node* cloneNode = new Node(node->val);
        map[node->val] = cloneNode;

        for (auto neighbor : node->neighbors) {
            cloneNode->neighbors.push_back(clone(neighbor, map));
        }

        return cloneNode;
    }
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