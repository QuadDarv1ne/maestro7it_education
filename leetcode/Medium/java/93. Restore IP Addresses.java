/*
https://leetcode.com/problems/restore-ip-addresses/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
    public List<String> restoreIpAddresses(String s) {
        /*
        Решение задачи "Restore IP Addresses" (LeetCode 93).

        Идея:
        - Backtracking на 4 сегмента.
        - Проверка на ведущие нули и допустимый диапазон.
        */
        List<String> res = new ArrayList<>();
        List<String> parts = new ArrayList<>();
        backtrack(s, 0, parts, res);
        return res;
    }

    private void backtrack(String s, int start, List<String> parts, List<String> res) {
        if (parts.size() == 4) {
            if (start == s.length())
                res.add(String.join(".", parts));
            return;
        }
        if (start >= s.length()) return;

        for (int len = 1; len <= 3 && start + len <= s.length(); len++) {
            String seg = s.substring(start, start + len);
            if (seg.length() > 1 && seg.charAt(0) == '0') continue;
            if (Integer.parseInt(seg) <= 255) {
                parts.add(seg);
                backtrack(s, start + len, parts, res);
                parts.remove(parts.size() - 1);
            }
        }
    }
}
