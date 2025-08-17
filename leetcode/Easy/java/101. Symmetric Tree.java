/**
 * https://leetcode.com/problems/symmetric-tree/description/
 */

/**
 * Класс решения задачи "Symmetric Tree".
 */
class Solution {
    /**
     * Проверяет зеркальную симметрию бинарного дерева.
     *
     * Алгоритм:
     * 1. Симметрия означает, что левое и правое поддерево — зеркальные.
     * 2. Используем рекурсивную проверку:
     *    - Если оба узла null → симметрия.
     *    - Если один null, а другой нет → асимметрия.
     *    - Если значения разные → асимметрия.
     *    - Рекурсивно проверяем пары (левый.левый ↔ правый.правый) и (левый.правый ↔ правый.левый).
     *
     * Время: O(n), где n — количество узлов.
     * Память: O(h), где h — глубина дерева (рекурсия).
     *
     * @param root корень дерева
     * @return true, если дерево симметрично, иначе false
     */
    public boolean isSymmetric(TreeNode root) {
        return isMirror(root, root);
    }

    /**
     * Вспомогательная функция для проверки зеркальной симметрии двух поддеревьев.
     */
    private boolean isMirror(TreeNode t1, TreeNode t2) {
        if (t1 == null && t2 == null) return true;
        if (t1 == null || t2 == null) return false;
        if (t1.val != t2.val) return false;

        return isMirror(t1.left, t2.right) && isMirror(t1.right, t2.left);
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