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

using System.Collections.Generic;

// public class TreeNode {
//     public int val;
//     public TreeNode left;
//     public TreeNode right;
//     public TreeNode(int val=0, TreeNode left=null, TreeNode right=null) {
//         this.val = val;
//         this.left = left;
//         this.right = right;
//     }
// }

public class Solution {
    // BFS подход
    public IList<int> RightSideView(TreeNode root) {
        var result = new List<int>();
        if (root == null) return result;
        
        var queue = new Queue<TreeNode>();
        queue.Enqueue(root);
        
        while (queue.Count > 0) {
            int levelSize = queue.Count;
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.Dequeue();
                
                if (i == levelSize - 1) {
                    result.Add(node.val);
                }
                
                if (node.left != null) queue.Enqueue(node.left);
                if (node.right != null) queue.Enqueue(node.right);
            }
        }
        return result;
    }
    
    // DFS подход
    public IList<int> RightSideViewDFS(TreeNode root) {
        var result = new List<int>();
        DFS(root, 0, result);
        return result;
    }
    
    private void DFS(TreeNode node, int depth, List<int> result) {
        if (node == null) return;
        
        if (depth == result.Count) {
            result.Add(node.val);
        }
        
        DFS(node.right, depth + 1, result);
        DFS(node.left, depth + 1, result);
    }
}