/**
 * https://leetcode.com/problems/symmetric-tree/description/
 */

/**
 * Определение структуры для узла бинарного дерева.
 * public class TreeNode {
 *     public int val;
 *     public TreeNode left;
 *     public TreeNode right;
 *     public TreeNode(int val = 0, TreeNode left = null, TreeNode right = null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */

public class Solution {
    /// <summary>
    /// Проверяет, является ли бинарное дерево зеркально симметричным относительно своего корня.
    ///
    /// Алгоритм:
    /// 1. Симметрия означает, что левое и правое поддерево должны быть зеркальными.
    /// 2. Используем рекурсивный метод IsMirror для проверки:
    ///    - Если оба узла равны null → симметрия.
    ///    - Если один равен null, а второй нет → асимметрия.
    ///    - Если значения узлов различаются → асимметрия.
    ///    - Иначе рекурсивно проверяем:
    ///         • левый потомок первого и правый потомок второго
    ///         • правый потомок первого и левый потомок второго
    ///
    /// Временная сложность: O(n), где n — количество узлов в дереве.
    /// Память: O(h), где h — глубина дерева (затраты на стек рекурсии).
    /// </summary>
    public bool IsSymmetric(TreeNode root) {
        return IsMirror(root, root);
    }

    /// <summary>
    /// Вспомогательная функция для проверки зеркальной симметрии двух поддеревьев.
    /// </summary>
    private bool IsMirror(TreeNode t1, TreeNode t2) {
        if (t1 == null && t2 == null) return true;
        if (t1 == null || t2 == null) return false;
        if (t1.val != t2.val) return false;

        return IsMirror(t1.left, t2.right) && IsMirror(t1.right, t2.left);
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