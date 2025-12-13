/*
https://leetcode.com/problems/restore-ip-addresses/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public IList<string> RestoreIpAddresses(string s) {
        /*
        Решение задачи "Restore IP Addresses" (LeetCode 93).

        Идея:
        - Backtracking: выбираем 4 сегмента по 1–3 цифры.
        - Проверяем на ведущие нули и значение ≤ 255.
        */
        var res = new List<string>();
        var parts = new List<string>();

        void Backtrack(int start) {
            if (parts.Count == 4) {
                if (start == s.Length)
                    res.Add(string.Join(".", parts));
                return;
            }
            if (start >= s.Length)
                return;

            for (int len = 1; len <= 3 && start + len <= s.Length; len++) {
                string seg = s.Substring(start, len);
                if (seg.Length > 1 && seg[0] == '0') continue;
                if (int.Parse(seg) <= 255) {
                    parts.Add(seg);
                    Backtrack(start + len);
                    parts.RemoveAt(parts.Count - 1);
                }
            }
        }

        Backtrack(0);
        return res;
    }
}
