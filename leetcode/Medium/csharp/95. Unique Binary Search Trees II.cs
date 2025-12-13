/*
https://leetcode.com/problems/unique-binary-search-trees-ii/description/

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
    public IList<TreeNode> GenerateTrees(int n) {
        /*
        Решение задачи "Unique Binary Search Trees II" (LeetCode 95).

        Идея:
        - Рекурсивная функция Build, генерирующая все BST
          для интервала [start..end].
        */
        if (n == 0) return new List<TreeNode>();
        return Build(1, n);
    }

    private IList<TreeNode> Build(int start, int end) {
        var trees = new List<TreeNode>();
        if (start > end) {
            trees.Add(null);
            return trees;
        }

        for (int i = start; i <= end; i++) {
            var leftTrees = Build(start, i - 1);
            var rightTrees = Build(i + 1, end);
            foreach (var l in leftTrees) {
                foreach (var r in rightTrees) {
                    var root = new TreeNode(i, l, r);
                    trees.Add(root);
                }
            }
        }
        return trees;
    }
}
