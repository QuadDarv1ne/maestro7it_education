/*
https://leetcode.com/problems/scramble-string/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public bool IsScramble(string s1, string s2) {
        int n = s1.Length;
        if (n != s2.Length) return false;

        int[] freq = new int[26];
        for (int i = 0; i < n; i++) {
            freq[s1[i]-'a']++;
            freq[s2[i]-'a']--;
        }
        foreach (int f in freq) if (f != 0) return false;

        // 3D DP
        bool[,,] dp = new bool[n, n, n+1];

        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                dp[i,j,1] = s1[i] == s2[j];

        for (int len = 2; len <= n; len++) {
            for (int i = 0; i+len <= n; i++) {
                for (int j = 0; j+len <= n; j++) {
                    for (int k = 1; k < len; k++) {
                        if ((dp[i,j,k] && dp[i+k,j+k,len-k]) ||
                            (dp[i,j+len-k,k] && dp[i+k,j,len-k])) {
                            dp[i,j,len] = true;
                            break;
                        }
                    }
                }
            }
        }
        return dp[0,0,n];
    }
}
