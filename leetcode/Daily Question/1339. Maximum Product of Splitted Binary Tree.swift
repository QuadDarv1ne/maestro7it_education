/**
 * Максимальное произведение разделенного бинарного дерева
 * 
 * @param root Корень бинарного дерева
 * @return Максимальное произведение сумм двух поддеревьев по модулю 10^9 + 7
 * 
 * Сложность: Время O(n), Память O(h), где n - количество узлов, h - высота дерева
 *
 * Автор: Дуплей Максим Игоревич
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

/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     public var val: Int
 *     public var left: TreeNode?
 *     public var right: TreeNode?
 *     public init() { self.val = 0; self.left = nil; self.right = nil; }
 *     public init(_ val: Int) { self.val = val; self.left = nil; self.right = nil; }
 *     public init(_ val: Int, _ left: TreeNode?, _ right: TreeNode?) {
 *         self.val = val
 *         self.left = left
 *         self.right = right
 *     }
 * }
 */

class Solution {
    private let MOD = 1_000_000_007
    private var maxProduct: Int64 = 0
    private var totalSum: Int64 = 0
    
    // Вычисление общей суммы всех узлов дерева
    private func calculateTotal(_ node: TreeNode?) -> Int64 {
        guard let node = node else { return 0 }
        return Int64(node.val) + calculateTotal(node.left) + calculateTotal(node.right)
    }
    
    // DFS для вычисления сумм поддеревьев и поиска максимального произведения
    private func dfs(_ node: TreeNode?) -> Int64 {
        guard let node = node else { return 0 }
        
        // Вычисление суммы текущего поддерева (постфиксный обход)
        let leftSum = dfs(node.left)
        let rightSum = dfs(node.right)
        let subtreeSum = Int64(node.val) + leftSum + rightSum
        
        // Если удалить ребро над текущим узлом, получим:
        // - Одно поддерево с суммой = subtreeSum
        // - Другое поддерево с суммой = totalSum - subtreeSum
        let product = subtreeSum * (totalSum - subtreeSum)
        maxProduct = max(maxProduct, product)
        
        return subtreeSum
    }
    
    func maxProduct(_ root: TreeNode?) -> Int {
        maxProduct = 0
        
        // Шаг 1: Вычисление общей суммы
        totalSum = calculateTotal(root)
        
        // Шаг 2: Поиск максимального произведения
        dfs(root)
        
        return Int(maxProduct % Int64(MOD))
    }
}