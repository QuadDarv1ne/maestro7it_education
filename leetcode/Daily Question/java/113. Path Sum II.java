/**
 * Поиск всех путей от корня к листьям с заданной суммой
 * 
 * @param root Корень бинарного дерева
 * @param targetSum Целевая сумма значений узлов в пути
 * @return Список всех путей, удовлетворяющих условию
 * 
 * Сложность: Время O(N), Память O(H) для рекурсии + O(N) для путей
 *
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
class Solution {
    public List<List<Integer>> pathSum(TreeNode root, int targetSum) {
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> currentPath = new ArrayList<>();
        dfs(root, targetSum, currentPath, result);
        return result;
    }
    
    private void dfs(TreeNode node, int targetSum, List<Integer> currentPath,
                     List<List<Integer>> result) {
        if (node == null) return;
        
        // Добавляем текущий узел в путь
        currentPath.add(node.val);
        
        // Проверяем, является ли узел листом с нужной суммой
        if (node.left == null && node.right == null && node.val == targetSum) {
            result.add(new ArrayList<>(currentPath));
        }
        
        // Рекурсивно обходим левое и правое поддеревья
        dfs(node.left, targetSum - node.val, currentPath, result);
        dfs(node.right, targetSum - node.val, currentPath, result);
        
        // Backtracking: удаляем текущий узел из пути
        currentPath.remove(currentPath.size() - 1);
    }
}