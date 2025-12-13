/*
https://leetcode.com/problems/binary-tree-inorder-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

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
    public IList<int> InorderTraversal(TreeNode root) {
        /*
        Решение задачи "Binary Tree Inorder Traversal" (LeetCode 94).

        Идея:
        - Итеративный обход через стек:
          сначала двигаемся влево, затем обрабатываем узлы.
        */
        var res = new List<int>();
        var stack = new Stack<TreeNode>();
        TreeNode curr = root;

        while (curr != null || stack.Count > 0) {
            while (curr != null) {
                stack.Push(curr);
                curr = curr.left;
            }
            curr = stack.Pop();
            res.Add(curr.val);
            curr = curr.right;
        }
        return res;
    }
}
