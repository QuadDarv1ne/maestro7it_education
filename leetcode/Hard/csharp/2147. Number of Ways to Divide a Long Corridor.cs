/*
https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public int NumberOfWays(string corridor) {
        const long MOD = 1000000007;
        var seats = new List<int>();

        for (int i = 0; i < corridor.Length; i++) {
            if (corridor[i] == 'S')
                seats.Add(i);
        }

        if (seats.Count < 2 || seats.Count % 2 != 0)
            return 0;

        long ways = 1;
        for (int i = 1; i < seats.Count - 1; i += 2) {
            long gap = seats[i + 1] - seats[i];
            ways = (ways * gap) % MOD;
        }

        return (int)ways;
    }
}
