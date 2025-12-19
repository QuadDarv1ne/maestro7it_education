/*
https://leetcode.com/problems/number-of-smooth-descent-periods-of-a-stock/description/?envType=daily-question&envId=2025-12-15

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Number of Smooth Descent Periods of a Stock"
*/

public class Solution {
    public long GetDescentPeriods(int[] prices) {
        int n = prices.Length;
        long ans = 0;
        long dp = 1;  // длина текущего smooth спада

        ans += dp;
        for (int i = 1; i < n; i++) {
            if (prices[i - 1] - prices[i] == 1) {
                dp++;
            } else {
                dp = 1;
            }
            ans += dp;
        }
        return ans;
    }
}
