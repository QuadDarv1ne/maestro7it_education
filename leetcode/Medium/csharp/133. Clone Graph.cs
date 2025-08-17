/**
 * https://leetcode.com/problems/clone-graph/description/
 */

/// <summary>
/// Определение узла графа.
/// </summary>
/*
public class Node
{
    public int val;
    public IList<Node> neighbors;
    public Node()
    {
        val = 0;
        neighbors = new List<Node>();
    }
    public Node(int _val)
    {
        val = _val;
        neighbors = new List<Node>();
    }
    public Node(int _val, IList<Node> _neighbors)
    {
        val = _val;
        neighbors = _neighbors;
    }
}
*/

public class Solution
{
    /// <summary>
    /// Клонирует связный неориентированный граф.
    /// Используется DFS с хэш-таблицей для отслеживания уже клонированных узлов.
    /// </summary>
    /// <param name="node">Узел графа, с которого начинается клонирование</param>
    /// <returns>Глубокая копия графа</returns>
    public Node CloneGraph(Node node)
    {
        if (node == null) return null;
        var map = new Dictionary<int, Node>();
        return Clone(node, map);
    }

    private Node Clone(Node node, Dictionary<int, Node> map)
    {
        if (map.ContainsKey(node.val)) return map[node.val];

        var clone = new Node(node.val);
        map[node.val] = clone;

        foreach (var neighbor in node.neighbors)
        {
            clone.neighbors.Add(Clone(neighbor, map));
        }

        return clone;
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